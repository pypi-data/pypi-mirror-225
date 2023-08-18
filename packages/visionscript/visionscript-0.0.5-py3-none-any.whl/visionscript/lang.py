import warnings

warnings.filterwarnings("ignore")

import copy
import io
import logging
import mimetypes
import os
import random
import shutil
import string
import sys
import time
import csv

import click
import cv2
import lark
import numpy as np
import psutil
import supervision as sv
import torch
import watchdog
from lark import Lark, UnexpectedCharacters, UnexpectedToken
from PIL import Image
from spellchecker import SpellChecker
from watchdog.observers import Observer

from visionscript import registry
from visionscript.grammar import grammar
from visionscript.paper_ocr_correction import (line_processing,
                                               syntax_correction)
from visionscript.usage import (USAGE, language_grammar_reference,
                                lowercase_language_grammar_reference)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_FILE_SIZE = 10000000  # 10MB

spell = SpellChecker()

parser = Lark(grammar, start="start")

SUPPORTED_INFERENCE_MODELS = {
    "groundingdino": lambda self, classes: registry.grounding_dino_base(self, classes),
    "yolov8": lambda self, classes: registry.yolov8_base(self, classes),
    "fastsam": lambda self, classes: registry.fast_sam_base(self, classes),
}

SUPPORTED_TRAIN_MODELS = {
    "vit": lambda self, folder: registry.vit_target(self, folder),
    "yolov8": lambda self, folder: registry.yolov8_target(self, folder),
}

STACK_MAXIMUM = {
    "image_stack": {
        # 50% of available memory
        "maximum": 0.5 * psutil.virtual_memory().available,
        "also_reset": ["detections_stack"],
    }
}

CONCURRENT_MAXIMUM = 10

VIDEO_STRIDE = 2


class InputNotProvided:
    pass


def handle_unexpected_characters(e, code, interactive=False):
    # if line doesn't end with ], add it
    if not code.strip().endswith("]"):
        code += "]"

        return

    # if space between statement and [, remove it
    # get position of [
    position = code.find("[")

    if code[position - 1] == " ":
        code = code[: position - 1] + code[position:]

        return

    # replace all “ with "
    code = code.replace("“", '"')
    code = code.replace("”", '"')

    # raise error if character not in grammar
    if e.char not in ["[", "]", "'", '"', ",", " ", '"', '"', "\n", "\t", "\r"]:
        print(f"Syntax error on line {e.line}, column {e.column}.")
        print(f"Unexpected character: {e.char!r}")
        exit(1)

    # raise error if class doesn't exist
    line = e.line
    column = e.column

    # check if function name in grammar
    function_name = code.strip().split("\n")[line - 1].split("[")[0].strip()

    language_grammar_reference_keys = language_grammar_reference.keys()

    if function_name in language_grammar_reference_keys:
        print(f"Syntax error on line {line}, column {column}.")
        print(f"Unexpected character: {e.char!r}")
        exit(1)

    spell.known(lowercase_language_grammar_reference)
    spell.word_frequency.load_words(lowercase_language_grammar_reference)

    alternatives = spell.candidates(function_name)

    if len(alternatives) == 0:
        print(f"Function {function_name} does not exist.")
        exit(1)

    print(f"Function '{function_name}' does not exist. Did you mean one of these?")
    print("-" * 10)

    for item in list(alternatives):
        if item.lower() in lowercase_language_grammar_reference:
            print(
                list(language_grammar_reference.keys())[
                    lowercase_language_grammar_reference.index(item.lower())
                ]
            )

    if interactive is False:
        exit(1)


def handle_unexpected_token(e, interactive=False):
    line = e.line
    column = e.column

    print(f"Syntax error on line {line}, column {column}.")
    print(f"Unexpected token: {e.token!r}")
    if interactive is False:
        exit(1)


def literal_eval(string):
    return string[1:-1] if string.startswith('"') and string.endswith('"') else string


def _get_colour_name(rgb_triplet):
    import webcolors

    min_colours = {}
    for key, name in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(name)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = key

    return min_colours[min(min_colours.keys())]


aliased_functions = {
    "isita": "classify",
    "find": "detect",
    "describe": "caption",
    "getcolors": "getcolours",
}


def map_alias_to_underlying_function(alias):
    return aliased_functions.get(alias, alias)


def init_state():
    return {
        "functions": {},
        "last_loaded_image": None,
        "last_loaded_image_name": None,
        "last": None,
        "last_function_type": None,
        "last_function_args": None,
        "image_stack": [],
        "detections_stack": [],
        "history": [],
        "search_index_stack": [],
        # "current_active_model": None,
        "output": None,
        "input_variables": {},
        "last_classes": [],
        "confidence": 50,
        "active_region": None,
        "active_filters": {"class": None, "region": None},
        "load_queue": [],
        "stack_size": {"image_stack": 0},
        "show_text_count": 0,
        "in_concurrent_context": False,
        "ctx": {},
        "tracker": None,
    }


class VisionScript:
    """
    A VisionScript program.
    """

    def __init__(self, notebook=False):
        self.state = init_state()
        self.notebook = notebook
        self.code = ""

        self.function_calls = {
            "load": lambda x: self.load(x),
            "save": lambda x: self.save(x),
            "classify": lambda x: self.classify(x),
            "size": lambda x: self.size(x),
            "say": lambda x: self.say(x),
            "detect": lambda x: self.detect(x),
            "segment": lambda x: self.segment(x),
            "cutout": lambda x: self.cutout(x),
            "count": lambda x: self.count(x),
            "countinregion": lambda x: self.countInRegion(*x),
            "replace": lambda x: self.replace(x),
            "in": lambda x: None,
            "if": lambda x: None,
            "var": lambda x: None,
            "variable": lambda x: None,
            "comment": lambda x: None,
            "expr": lambda x: None,
            "show": lambda x: self.show(x),
            "exit": lambda x: exit(0),
            "help": lambda x: print(language_grammar_reference[x]),
            "train": lambda x: self.train(x),
            "compare": lambda x: self.show(x),
            "read": lambda x: self.read(x),
            "label": lambda x: self.label(x),
            "list": lambda x: None,
            "get": lambda x: self.get_func(x),
            "use": lambda x: self.set_state("current_active_model", x),
            "caption": lambda x: self.caption(x),
            "contains": lambda x: self.contains(x),
            "import": lambda x: self.import_(x),
            "rotate": lambda x: self.rotate(x),
            "getcolours": lambda x: self.getcolours(x),
            "get_text": lambda x: self.get_text(x),
            "greyscale": lambda x: self.greyscale(x),
            "select": lambda x: self.select(x),
            "paste": lambda x: self.paste(x),
            "pasterandom": lambda x: self.pasterandom(x),
            "resize": lambda x: self.resize(x),
            "blur": lambda x: self.blur(x),
            "make": lambda x: self.make(x),
            "args": lambda x: None,
            "setbrightness": lambda x: self.set_brightness(x),
            "search": lambda x: self.search(x),
            "similarity": lambda x: self.similarity(x),
            "readqr": lambda x: self.read_qr(x),
            "reset": lambda x: self.reset(x),
            "negate": lambda x: self.negate(x),
            "equality": lambda x: self.equality(x),
            "not_equality": lambda x: not self.equality(x),
            "input": lambda x: self.input_(x),
            "deploy": lambda x: self.deploy(x),
            "getedges": lambda x: self.get_edges(x),
            "setregion": lambda x: self.set_region(x),
            "setconfidence": lambda x: self.set_confidence(x),
            "filterbyclass": lambda x: self.filter_by_class(x),
            "crop": lambda x: self.crop(x),
            "shuffle": lambda x: self.shuffle(x),
            "grid": lambda x: self.grid(x),
            "run": lambda x: self.parse_tree(parser.parse(self.state["last"])),
            "showtext": lambda x: self.show_text(x),
            "getfps": lambda x: self.state["ctx"].get("fps", 0)
            if self.state["ctx"]["in"] is not None
            else 0,
            "gt": lambda x: x[0] > x[1],
            "gte": lambda x: x[0] >= x[1],
            "lt": lambda x: x[0] < x[1],
            "lte": lambda x: x[0] <= x[1],
            "track": lambda x: self.track(x),
            "getdistinctscenes": lambda x: self.get_distinct_scenes(x),
            "getuniqueappearances": lambda x: self.get_unique_appearances(x),
        }

    def countInRegion(self, class_, x0, y0, x1, y1):
        """
        Count the number of detections of a class in a region.
        """
        # count predictions from top of stack in region

        predictions = self._get_item(-1, "detections_stack")

        if predictions is None:
            return 0

        zone = sv.PolygonZone(
            polygon=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        )

        detections = sv.Detections(predictions)
        results = zone.trigger(detections=detections)

        # count number of True values in the "results" list
        return len([x for x in results if x])

    def filter_by_class(self, args):
        """
        Filter detections by class.
        """
        if len(args) == 0:
            self.state["active_filters"] = None
        elif self.state["active_filters"].get("class") is None:
            self.state["active_filters"]["class"] = args

    def set_region(self, args):
        if len(args) == 0:
            self.state["active_filters"]["region"] = None
            return

        x0, y0, x1, y1 = args

        self.state["active_filters"]["region"] = (x0, y0, x1, y1)

    def input_(self, key):
        if self.state["input_variables"].get(literal_eval(key)) is not None:
            return self.state["input_variables"][literal_eval(key)]
        else:
            return InputNotProvided()

    def equality(self, args):
        return args[0] == args[1]

    def negate(self, expr):
        return not expr

    def reset(self, _):
        self.state = init_state()

    def set_state(self, key, value):
        self.state[key] = value

    def make(self, args):
        """
        Declare a function.
        """
        function_name = args[0].children[0].value.strip()

        function_body = lark.Tree("expr", args[1:])

        self.state["functions"][function_name] = function_body

    def set_confidence(self, confidence):
        """
        Set the confidence level for use in filtering detections.
        """
        if not confidence:
            confidence = 50

        if confidence > 100 or confidence < 0:
            print("Confidence must be between 0 and 100.")
            return

        self.state["confidence"] = confidence

    def track(self, _):
        self.state["tracker"] = sv.ByteTrack()

    def get_distinct_scenes(self, _):
        if not self.state.get("video_events_from_Classify[]"):
            return []
        
        scenes = self.state["video_events_from_Classify[]"]

        scene_changes = []

        fps = self.state["ctx"].get("fps", 0)

        # show timestamp in seconds

        # whenever a "text" value changes for 2 or more frames, we have a scene change
        for i in range(1, len(scenes)):
            if len(i) < 2:
                continue

            N = 10

            last_n_scenes = scenes[i-N:i]

            last_scene = last_n_scenes[-1]

            # get most common object in last 5 scenes
            most_common_object = max(set(last_n_scenes), key=last_n_scenes.count)

            if last_scene["text"] != most_common_object:
                current_frame_in_seconds = i / fps
                scene_changes.append({"text": last_scene["text"], "frame": i * VIDEO_STRIDE, "time": current_frame_in_seconds})
        
        return scene_changes
    
    def get_unique_appearances(self, class_name):
        if class_name:
            class_id = self.state["last_classes"].index(class_name)
            results = self.state["tracker"].tracker_id[self.state["tracker"].class_id == class_id]
        else:
            results = self.state["tracker"].tracker_id

        return max(results)

    def load_queue(self, items):
        """
        Load a queue of images into state.
        """
        self.state["load_queue"].append(items)

    def load(self, filename):
        """
        Load an image or folder of images into state.
        """
        import requests
        import validators

        # if session_id and notebook, concatenate tmp/session_id/ to filename

        if isinstance(filename, np.ndarray):
            self._add_to_stack("image_stack", filename)
            # save file
            import uuid

            name = str(uuid.uuid4()) + ".png"
            cv2.imwrite(name, filename)

            self.state["last_loaded_image_name"] = name

            return filename

        # if is dir, load all images
        if filename and os.path.isdir(filename):
            image_filenames = [filename + "/" + item for item in os.listdir(filename)]

            for image_filename in image_filenames:
                self.load(image_filename)

            return

        if filename and validators.url(filename):
            try:
                response = requests.get(filename, timeout=5, stream=True)
            except requests.exceptions.ConnectionError:
                self.state["last"] = "Could not connect to URL."
                return
            except requests.exceptions.ReadTimeout:
                self.state["last"] = "Timeout."
                return
            except:
                self.state["last"] = "There was an error loading the image."
                return

            # check length
            if len(response.content) > MAX_FILE_SIZE:
                self.state["last"] = "Image too large."
                return

            size = 0
            start = time.time()

            for chunk in response.iter_content(1024):
                if time.time() - start > 5:
                    raise ValueError("timeout reached")

                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    raise ValueError("response too large")

            file_extension = mimetypes.guess_extension(response.headers["content-type"])

            # if not image, error
            if file_extension not in (".png", ".jpg", ".jpeg"):
                print(f"File {filename} does not represent a png, jpg, or jpeg image.")
                return None

            # 10 random characters
            filename = (
                "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(10)
                )
                + file_extension
            )

            # mk session dir + tmp if needed
            if not os.path.exists("tmp"):
                os.makedirs("tmp")

            if not os.path.exists(os.path.join("tmp", self.state["session_id"])):
                os.makedirs(os.path.join("tmp", self.state["session_id"]))

            # save to tmp
            with open(
                os.path.join("tmp", self.state["session_id"], filename), "wb"
            ) as f:
                f.write(response.content)

            filename = os.path.join("tmp", self.state["session_id"], filename)

        if self.state.get("ctx") and self.state["ctx"].get("in"):
            filename = self.state["ctx"]["active_file"]
        elif (
            self.state.get("ctx")
            and self.state["ctx"].get("in")
            and isinstance(self.state["ctx"]["active_file"], np.ndarray)
        ):
            # if in video context, frame is already loaded
            self.state["output"] = {"image": self.state["ctx"]["active_file"]}

            return self.state["ctx"]["active_file"]

        from werkzeug.utils import secure_filename

        filename = filename.split("/")[-1]

        filename = secure_filename(filename)

        filename = filename.strip()

        # if extension is not in jpg, png, jpeg, do fuzzy
        if not filename.endswith((".jpg", ".png", ".jpeg")):
            # fuzzy search
            from fuzzywuzzy import process

            image_filenames = [
                item
                for item in os.listdir(".")
                if item.endswith((".jpg", ".png", ".jpeg"))
            ]

            if not image_filenames:
                print("No images found in tmp directory.")
                return

            image_filenames = [item.split(".")[0] for item in image_filenames]

            image_filename = process.extractOne(filename, image_filenames)[0]

            filename = image_filename + ".png"

            self.state["last_loaded_image_name"] = filename

        try:
            if self.notebook and (
                not validators.url(filename) or filename.endswith(".png")
            ):
                print("notebook")
                filename = os.path.join("tmp", self.state["session_id"], filename)

            image = Image.open(filename).convert("RGB")
        except Exception as e:
            print(e)
            print(f"Could not load image {filename}.")
            return

        self.state["last_loaded_image_name"] = filename

        self.state["output"] = {"image": image}

        return np.array(image), filename

    def size(self, _):
        return self._get_item(-1, "image_stack").shape[:2]

    def import_(self, args):
        """
        Import a module from another file.
        """
        # this will update self.state for the entire script

        file_name = "".join(
            [
                letter
                for letter in args
                if letter.isalpha() or letter == "-" or letter.isdigit()
            ]
        )

        with open(file_name + ".vic", "r") as f:
            code = f.read()

        tree = parser.parse(code.strip() + "\n")

        self.parse_tree(tree)

    def cutout(self, _):
        """
        Cut out a detection from an image.
        """
        if len(self.state["last"].xyxy) == 0:
            return

        x1, y1, x2, y2 = self.state["last"].xyxy[0]
        image = self._get_item(-1, "image_stack")
        # if image is ndarray, convert to PIL image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        cropped_image = image.crop((x1, y1, x2, y2))

        # convert back to ndarray
        cropped_image = np.array(cropped_image)

        self._add_to_stack("image_stack", cropped_image)

        self.state["output"] = {"image": cropped_image}
        return [cropped_image]

    def crop(self, args):
        """
        Crop an image.
        """
        image = self._get_item(-1, "image_stack")

        # if ndarray, convert to PIL image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        if len(args) == 0:
            image = image.crop((0, 0, image.size[0] // 2, image.size[1] // 2))
        else:
            x0, y0, x1, y1 = args

            x0 = int(x0) if isinstance(x0, str) else x0
            y0 = int(y0) if isinstance(y0, str) else y0
            x1 = int(x1) if isinstance(x1, str) else x1
            y1 = int(y1) if isinstance(y1, str) else y1

            image = image.crop((x0, y0, x1, y1))

        self._add_to_stack("image_stack", image)

    def select(self, args):
        """
        Select a detection from a sv.Detections object.
        """
        # if detect, select from detections
        if self.state.get("last_function_type", None) in (
            "detect",
            "segment",
            "classify",
        ):
            detections = self.state["last"]

            detections = self._filter_controller(detections)

            if len(args) == 0:
                self.state["last"] = detections
            else:
                self.state["last"] = detections[args[0]]

    def paste(self, args):
        """
        Paste an image onto another image.
        """
        x, y = args
        self._add_to_stack(
            "image_stack",
            self.state["image_stack"][-2].paste(
                self._get_item(-1, "image_stack"), (x, y)
            ),
        )

    def resize(self, args):
        """
        Resize an image.
        """
        width, height = args
        image = self._get_item(-1, "image_stack")
        image = cv2.resize(image, (width, height))
        self._add_to_stack("image_stack", image)

    def grid(self, n):
        """
        Divide into a grid of N images.
        """
        if not n:
            n = 9

        image = self._get_item(-1, "image_stack")

        height, width, _ = image.shape

        # divide into n equal boxes with w and h
        images = []

        for i in range(n):
            images.append(
                image[
                    (height // n) * i : (height // n) * (i + 1),
                    (width // n) * i : (width // n) * (i + 1),
                ]
            )

        # remove last image from stack
        self.state["image_stack"].pop()

        self.state["image_stack"].extend(images)

    def shuffle(self, _):
        """
        Shuffle images on the stack.
        """
        random.shuffle(self.state["image_stack"])

    def _create_index(self):
        import faiss

        index = faiss.IndexFlatL2(512)

        self.state["search_index_stack"].append(index)

        return index

    def _add_to_index(self, image):
        index = self.state["search_index_stack"][-1]

        index.add(image)

    def search(self, label):
        """
        Search for an image using a text label or image.

        On first run, this will create an index of all images on the loaded image stack.
        """
        import clip

        model, preprocess = clip.load("ViT-B/32", device=DEVICE)

        with torch.no_grad():
            # if label is a filename, load image
            if os.path.exists(label):
                comparator = preprocess(Image.open(label)).unsqueeze(0).to(DEVICE)

                comparator = model.encode_image(comparator)
            else:
                comparator = clip.tokenize([label]).to(DEVICE)

                comparator = model.encode_text(comparator)

            if len(self.state["search_index_stack"]) == 0:
                self._create_index()

                for image in self.state["image_stack"]:
                    # turn cv2 image into PIL image
                    image = Image.fromarray(image)

                    processed_image = preprocess(image).unsqueeze(0).to(DEVICE)
                    embedded_image = model.encode_image(processed_image)

                    self._add_to_index(embedded_image)

        index = self.state["search_index_stack"][-1]

        results = index.search(comparator, 5)

        image_names = []

        for result in results[1][0]:
            image_names.append(self.state["image_stack"][result])

        if len(self.state["image_stack"]) < 5:
            image_names = image_names[: len(self.state["image_stack"])]

        return image_names

    def pasterandom(self, _):
        """
        Paste the most recent image in a random position on the previously most recent image.
        """
        x, y = []

        while True:
            x, y = random.randint(0, self.state["image_stack"].size[0]), random.randint(
                0, self.state["image_stack"].size[1]
            )

            if len(self.state["last"].xyxy) == 0:
                break

            for bbox in self.state["last"].xyxy:
                x1, y1, x2, y2 = bbox

                if x1 <= x <= x2 and y1 <= y <= y2:
                    continue

            break

        self.state["image_stack"][-1] = self.state["image_stack"][-2].paste(
            self._get_item(-1, "image_stack"), (x, y)
        )

    def save(self, filename):
        """
        Save an image to a file.
        """
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        if not os.path.exists("tmp/output"):
            os.makedirs("tmp/output")

        if not filename:
            filename = os.path.join(
                "tmp/output/",
                "".join(random.choice(string.ascii_letters) for _ in range(10)),
            )

        if filename.endswith(".csv"):
            self.write_to_csv(filename)

            return

        if self.state.get("history", None) and "camera" in self.state["history"]:
            video = cv2.VideoWriter(
                filename + ".avi",
                cv2.VideoWriter_fourcc(*"MJPG"),
                10,
                (640, 480),
            )

            for image in self.state["image_stack"]:
                video.write(image)

            video.release()

            # check if ffmpeg is installed
            # if it is, convert to mp4
            if shutil.which("ffmpeg"):
                os.system(
                    f"ffmpeg -i {filename}.avi -vcodec h264 -acodec mp2 {filename}.mp4 > /dev/null 2>&1"
                )

        self.state["image_stack"].save(filename)

        self.state["output"] = {"text": "Saved to " + filename}

    def count(self, args):
        """
        Count the number of detections in a sv.Detections object.
        """

        if len(args) == 0 and isinstance(
            self.state["last"], sv.detection.core.Detections
        ):
            return len(self.state["last"].confidence)
        else:
            return len(args)

    def greyscale(self, _):
        """
        Turn an image to greyscale.
        """
        image = self._get_item(-1, "image_stack")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self._add_to_stack("image_stack", image)

        self.state["output"] = {"image": image}

    def deploy(self, app_name):
        """
        Deploy a script to a VisionScript Cloud web app.
        """
        # make POST to http://localhost:6999/create
        import string

        import requests

        app_slug = app_name.translate(
            str.maketrans("", "", string.punctuation.replace("-", ""))
        ).replace(" ", "-")

        response = requests.post(
            "http://localhost:6999/create",
            json={
                "api_key": "test",
                "title": app_name,
                "slug": app_slug,
                "script": self.code,
                "variables": self.state["input_variables"],
            },
        )

        if response.ok:
            return "Deployed successfully to http://localhost:6999/app"

        return "Error deploying."

    def get_text(self, _):
        """
        Use OCR to get text from an image.
        """
        # if not in notebook
        if self.state.get("notebook", False):
            from google.cloud import vision

            # do handwriting detection
            client = vision.ImageAnnotatorClient()

            with io.open(self.state["last_loaded_image_name"], "rb") as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            # Load[Detect[dog]]Show[]
            # Load[] Detect[dog] Show[]
            # Load[dog.png] Detect[dog] Show[]

            response = client.document_text_detection(image=image)

            result = ""

            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            result += "".join([symbol.text for symbol in word.symbols])

            result = line_processing(result)
            result = syntax_correction(result)

        else:
            import easyocr

            reader = easyocr.Reader(["en"])
            result = reader.readtext(self.state["last_loaded_image_name"], detail=0)

        # import pytesseract

        # result = pytesseract.image_to_string(self.state["last_loaded_image_name"], config='--user-patterns patterns.txt')

        # print(result, "result")

        self.state["output"] = {"text": result}
        self.state["last"] = result

        return result

    def rotate(self, args):
        """
        Rotate an image.
        """
        image = self._get_item(-1, "image_stack")
        # load into cv2
        args = int(args)
        if args == 90:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif args == 180:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif args == 270:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            image = image

        self.state["output"] = {"image": image}
        self._add_to_stack("image_stack", image)

    def getcolours(self, k):
        """
        Get the most common colours in an image.
        """
        if not k:
            k = 1

        from sklearn.cluster import KMeans

        image = self._get_item(-1, "image_stack")

        image = np.array(image)

        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clt = KMeans(n_clusters=k)

        clt.fit(image)

        # map to human readable colour
        centers = clt.cluster_centers_

        human_readable_colours = []

        for center in centers:
            try:
                human_readable_colours.append(
                    _get_colour_name((int(center[0]), int(center[1]), int(center[2])))
                )
            except ValueError as e:
                continue

        self.state["last"] = human_readable_colours[:k]

        return human_readable_colours[:k]

    def _filter_controller(self, detections):
        results = detections

        if self.state["active_filters"]["region"]:
            x0, y0, x1, y1 = self.state["active_filters"]["region"]

            zone = sv.PolygonZone(
                np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]),
                frame_resolution_wh=(
                    self.state["last"].shape[1],
                    self.state["last"].shape[0],
                ),
            )

            results_filtered_by_active_region = zone.trigger(detections=results)

            results = results[results_filtered_by_active_region]

        if self.state["active_filters"]["class"]:
            results = results[
                np.isin(results.class_id, self.state["active_filters"]["class"])
            ]

        results = results[results.confidence > self.state["confidence"] / 100]

        # self.state["last"] = results

        return results

    def detect(self, classes):
        """
        Run object detection on an image.
        """
        logging.disable(logging.CRITICAL)

        if self.state.get("current_active_model") is None:
            self.state["current_active_model"] = "yolov8"

        self.state["current_active_model"] = self.state["current_active_model"].lower()

        results, inference_classes = SUPPORTED_INFERENCE_MODELS[
            self.state["current_active_model"]
        ](self, classes)

        # swap keys and values
        inference_classes_as_idx = {v: k for k, v in inference_classes.items()}

        class_idxes = [inference_classes_as_idx.get(i, -1) for i in classes.split(",")]

        results = results[np.isin(results.class_id, class_idxes)]

        self._add_to_stack("detections_stack", results)
        self.state["last_classes"] = [
            inference_classes[i] for i in class_idxes if i != -1
        ]

        self.state["last"] = results

        return results
    
    def write_to_csv(self, name):
        if isinstance(self.state["last"], sv.Detections):
            xyxy = self.state["last"].xyxy
            conf = self.state["last"].confidence
            class_ids = self.state["last"].class_id
            class_names = [self.state["last_classes"][i] for i in class_ids]

            csv_record = list(zip(xyxy, conf, class_ids, class_names))

            write_header_row = True if not os.path.exists(name) else False

            with open(name, "w") as f:
                writer = csv.writer(f)
                if write_header_row:
                    writer.writerow(
                        [
                            "x0",
                            "y0",
                            "x1",
                            "y1",
                            "confidence",
                            "class_id",
                            "class_name",
                        ]
                    )

                writer.writerows(csv_record)

    def classify(self, labels):
        """
        Classify an image using provided labels.
        """
        image = self.state["last"]

        if self.state.get("model") and self.state["model"].__class__.__name__ == "ViT":
            model = self.state["model"]

            results = model.predict(image).get_top_k(1)

            if len(results.class_id) == 0:
                return sv.Classifications.empty()

            return results.class_id[0]
        elif (
            self.state.get("model")
            and self.state["model"].__class__.__name__ == "YOLOv8"
        ):
            model = self.state["model"]

            results = model.predict(image)

            return results

        import clip

        model, preprocess = clip.load("ViT-B/32", device=DEVICE)

        image = (
            preprocess(Image.open(self.state["last_loaded_image_name"]))
            .unsqueeze(0)
            .to(DEVICE)
        )
        text = clip.tokenize(labels).to(DEVICE)

        with torch.no_grad():
            logits_per_image, _ = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            # get idx of the most likely label class
            label_idx = probs.argmax()

            label_name = labels[label_idx]

        self.state["output"] = {"text": label_name}

        if self.state["ctx"].get("video_events_from_Classify[]"):
            self.state["ctx"]["video_events_from_Classify[]"].append(
                {"text": label_name, "frame": self.state["ctx"]["current_frame_count"]}
            )

        return label_name

    def segment(self, text_prompt):
        """
        Apply image segmentation and generate segmentation masks.
        """
        # check for model
        if self.state.get("current_active_model") is None:
            self.state["current_active_model"] = "fastsam"

        detections = SUPPORTED_INFERENCE_MODELS[self.state["current_active_model"]](
            self, text_prompt
        )

        if self.state["tracker"]:
            # use bytetrack for object tracking
            detections = self.state["tracker"].update_with_detections(detections)

        # load last_loaded_image_name
        image = cv2.imread(self.state["last_loaded_image_name"])

        # cut out all detections and save them to the state
        for _, detection in enumerate(detections.xyxy):
            x1, y1, x2, y2 = detection
            self._add_to_stack("image_stack", image[y1:y2, x1:x2])

        self.state["last"] = self._get_item(-1, "image_stack")

        self._add_to_stack("detections_stack", detections)

        return detections

    def read(self, _):
        if self.state.get("last_function_type", None) in ("detect", "segment"):
            last_args = self.state["last_function_args"]
            statement = "".join(
                [
                    f"{last_args[0]} {self.state['last'].confidence[i]:.2f} {self.state['last'].xyxy[i]}\n"
                    for i in range(len(self.state["last"].xyxy))
                ]
            )

            return statement

        return str(self.state["last"])

    def say(self, statement):
        """
        Print a statement to the console, or create a text representation of a statement for use
        in a notebook.
        """

        if isinstance(self.state["last"], np.ndarray):
            self.show(None)
            return

        if isinstance(self.state["last"], int):
            print(str(self.state["last"]))
            return

        if isinstance(self.state["last"], (list, tuple)):
            output = ""

            for item in self.state["last"]:
                # if list or tuple, join
                if isinstance(item, (list, tuple)):
                    item = ", ".join([str(i) for i in item])
                elif isinstance(item, int) or isinstance(item, float):
                    item = str(item)

                output += item + "\n"

            self.state["output"] = {"text": output}

            return statement.strip()

        if isinstance(statement, int) or isinstance(statement, float):
            statement = str(statement)

        if statement and isinstance(statement, str):
            print(statement.strip())
            return statement.strip()

        if isinstance(self.state["last"], sv.Detections):
            last_args = self.state["last_function_args"]
            statement = "".join(
                [
                    f"{last_args} {self.state['last'].confidence[i]:.2f} {self.state['last'].xyxy[i]}\n"
                    for i in range(len(self.state["last"].xyxy))
                ]
            )
        elif isinstance(self.state["last"], list):
            statement = ", ".join([str(item) for item in self.state["last"]])
        else:
            statement = self.state["last"]

        if statement:
            print(statement.strip())

        self.state["output"] = {"text": statement}
        self.state["last"] = statement

    def show_text(self, text):
        if not text and isinstance(self.state["last"], str):
            text = self.state["last"]

        # add text to the last frame
        image = self._get_item(-1, "image_stack")

        position = (20, image.shape[0] // 10)

        if self.state["show_text_count"] > 0:
            position = (self.state["show_text_count"] + 20, position[1])

        # create background box
        image = cv2.rectangle(
            image,
            (position[0], position[1] - 30),
            (position[0] + len(text) * 20, position[1] + 10),
            (0, 0, 0),
            -1,
        )

        image = cv2.putText(
            image,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        if text and len(text) > 0:
            self.state["show_text_count"] = len(text)

        self._add_to_stack("image_stack", image)

    def blur(self, args):
        """
        Blur an image.
        """

        image = self._get_item(-1, "image_stack")

        image = cv2.blur(image, (args[0], args[0]))

        self._add_to_stack("image_stack", image)

    def replace(self, args):
        """
        Replace a detection or list of detections with an image or color.
        """
        detections = self.state["last"]

        detections = self._filter_controller(detections)

        xyxy = detections.xyxy

        if os.path.exists(args):
            picture = cv2.imread(args)

            # bgr to rgb
            picture = picture[:, :, ::-1].copy()

            image_at_top_of_stack = self._get_item(-1, "image_stack").copy()

            for i in range(len(xyxy)):
                x1, y1, x2, y2 = xyxy[i]

                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # resize picture to fit
                picture = cv2.resize(picture, (x2 - x1, y2 - y1))

                image_at_top_of_stack[y1:y2, x1:x2] = picture

            self._add_to_stack("image_stack", image_at_top_of_stack)

            return

        color = args

        if args is not None:
            import webcolors

            try:
                color_to_rgb = webcolors.name_to_rgb(color)
            except ValueError:
                print(f"Color {color} does not exist.")
                return

            color_to_rgb = np.array(color_to_rgb)

            # convert to bgr
            color_to_rgb = color_to_rgb[::-1]

            for i in range(len(xyxy)):
                x1, y1, x2, y2 = xyxy[i]

                # cast all to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                self._get_item(-1, "image_stack")[y1:y2, x1:x2] = color_to_rgb

    def label(self, args):
        """
        Label a folder of images using an object detection, classification, or segmentation model.

        Not fully implemented.
        """
        folder = args[0]
        items = args[2]

        if (
            "Detect" in self.state["history"]
            or self.state["current_active_model"] == "groundedsam"
        ):
            from autodistill.detection import CaptionOntology
            from autodistill_grounded_sam import GroundedSAM

            mapped_items = {item: item for item in items}

            base_model = GroundedSAM(CaptionOntology(mapped_items))
        else:
            print("Please specify a model with which to label images.")
            return

        base_model.label(folder)

    def caption(self, _):
        """
        Generate a caption for an image.
        """
        from transformers import BlipForConditionalGeneration, BlipProcessor

        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        inputs = processor(self._get_item(-1, "image_stack"), return_tensors="pt")

        out = model.generate(**inputs)

        self.state["last"] = processor.decode(out[0], skip_special_tokens=True)

        return processor.decode(out[0], skip_special_tokens=True)

    def train(self, args):
        """
        Train a model on a dataset.

        Not fully implemented.
        """
        folder = args[0]
        model = args[1]

        # if Detect or Classify run, train
        if "Detect" in self.state["history"] or model == "yolov8":
            self.state["current_active_model"] = "yolov8n"
        elif "Classify" in self.state["history"] or model == "vit":
            self.state["current_active_model"] = "vit"
        else:
            print("No training needed.")
            return

        self.state["model"] = SUPPORTED_TRAIN_MODELS[model](self, folder)

    def get_edges(self, _):
        """
        Convert image to greyscale then perform Sobel edge detection.
        """
        self.greyscale(_)

        image = self._get_item(-1, "image_stack")

        sobelxy = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=5)

        self._add_to_stack("image_stack", sobelxy)
        self.state["output"] = {"image": sobelxy}

    def _enforce_stack_maximums(self, stack, item=None):
        # this was built in particular to prevent the image stack from growing too large
        if item is not None:
            stack_size = self.state["stack_size"].get(stack, 0)

            # get amount of memory used by item
            # if item is a numpy array, get its size in bytes
            if isinstance(item, np.ndarray):
                stack_size += item.nbytes
            elif isinstance(item, list):
                for i in item:
                    if isinstance(i, np.ndarray):
                        stack_size += i.nbytes
            elif isinstance(item, dict):
                for i in item.values():
                    if isinstance(i, np.ndarray):
                        stack_size += i.nbytes
            elif isinstance(item, str):
                stack_size += os.path.getsize(item)
            else:
                stack_size += sys.getsizeof(item)

            # if stack size is greater than maximum, remove items from stack
            if (
                STACK_MAXIMUM.get(stack, None)
                and stack_size > STACK_MAXIMUM.get(stack)["maximum"]
            ):
                # remove items from stack until stack size is less than maximum
                while stack_size > STACK_MAXIMUM.get(stack)["maximum"]:
                    # remove first last item from stack
                    removed_item = self.state[stack].pop(0)

                    # subtract size of removed item from stack size
                    stack_size -= removed_item.nbytes

        if (
            STACK_MAXIMUM.get(stack, None)
            and len(self.state[stack]) > STACK_MAXIMUM.get(stack)["maximum"]
        ):
            self.state[stack] = self.state[stack][
                -STACK_MAXIMUM.get(stack)["maximum"] :
            ]

            for also_reset in STACK_MAXIMUM.get(stack)["also_reset"]:
                self.state[also_reset] = self.state[also_reset][
                    -STACK_MAXIMUM.get(stack)["maximum"] :
                ]

    def _add_to_stack(self, stack, item):
        self.state[stack].append(item)

        self._enforce_stack_maximums(stack, item)

    def _get_item(self, n=1, stack="image_stack"):
        # get() overwrites n

        if self.state.get("get", None):
            n = self.state["get"]

        self._enforce_stack_maximums(stack, None)

        # if len() of load_queue > image_stack, load next image
        if len(self.state["load_queue"]) > len(self.state["image_stack"]):
            for filename in self.state["load_queue"][len(self.state["image_stack"]) :]:
                self.state["image_stack"].append(cv2.imread(filename))

        return self.state[stack][n]

    def show(self, _):
        """
        Show the image in the notebook or in a new window.

        If a Detect or Segment function was run previously, this function shows the image with the bounding boxes.
        """

        image = self._get_item(-1, "image_stack")

        if "detect" in self.state["history"]:
            annotator = sv.BoxAnnotator()
        elif "segment" in self.state["history"]:
            annotator = sv.MaskAnnotator()
        else:
            annotator = None

        if (
            self.state.get("last_loaded_image_name") is None
            or not os.path.exists(self.state["last_loaded_image_name"])
        ) and self.state["ctx"].get("in") is None:
            print("Image does not exist.")
            return

        def get_divisors(n):
            divisors = []

            for i in range(1, n + 1):
                if n % i == 0:
                    divisors.append(i)

            return divisors

        def get_closest_divisor(n):
            divisors = get_divisors(n)

            return divisors[len(divisors) // 2]

        grid_size = get_closest_divisor(len(self.state["image_stack"]))

        # if there was a grid before a reset
        last_reset_idx = (
            self.state["history"].index("reset")
            if "reset" in self.state["history"]
            else 0
        )
        last_grid_idx = (
            self.state["history"].index("grid")
            if "grid" in self.state["history"]
            else 0
        )

        if last_grid_idx > last_reset_idx:
            images = []

            for image in self.state["image_stack"]:
                images.append(np.array(image))

            # reassemble
            # get dims in last image
            smallest_dims = 3

            for image in images:
                if len(image.shape) < smallest_dims:
                    smallest_dims = len(image.shape)

            image = np.zeros(
                (
                    images[0].shape[0] * grid_size,
                    images[0].shape[1] * grid_size,
                    smallest_dims,
                ),
                dtype=np.uint8,
            )

            for i in range(grid_size):
                for j in range(grid_size):
                    image[
                        i * images[0].shape[0] : (i + 1) * images[0].shape[0],
                        j * images[0].shape[1] : (j + 1) * images[0].shape[1],
                    ] = images[i * grid_size + j]

            # return image
            cv2.imshow("image", np.array(image))
            cv2.waitKey(0)

            return

        if self.state.get("history", [])[-1] == "compare":
            images = []

            def get_divisors(n):
                divisors = []

                for i in range(1, n + 1):
                    if n % i == 0:
                        divisors.append(i)

                return divisors

            def get_closest_divisor(n):
                divisors = get_divisors(n)

                return divisors[len(divisors) // 2]

            grid_size = get_closest_divisor(len(self.state["image_stack"]))

            # if there was a grid before a reset
            last_reset_idx = (
                self.state["history"].index("reset")
                if "reset" in self.state["history"]
                else 0
            )
            last_grid_idx = (
                self.state["history"].index("grid")
                if "grid" in self.state["history"]
                else 0
            )

            if last_grid_idx > last_reset_idx:
                for image in self.state["image_stack"]:
                    images.append(np.array(image))

            for image, detections in zip(
                self.state["image_stack"], self.state["detections_stack"]
            ):
                detections = self._filter_controller(detections)
                if annotator and detections and isinstance(annotator, sv.BoxAnnotator):
                    image = annotator.annotate(
                        np.array(image), detections, labels=self.state["last_classes"]
                    )
                elif annotator and detections:
                    image = annotator.annotate(np.array(image), detections)
                else:
                    image = np.array(image)

                images.append(image)

            if not self.notebook:
                sv.plot_images_grid(
                    images=np.array(images),
                    grid_size=(grid_size, grid_size),
                    size=(12, 12),
                )

                return

            # image = images[0]

        if annotator:
            # turn (self._get_item(-1, "image_stack")) into RGB
            image = np.array(self._get_item(-1, "image_stack"))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if isinstance(annotator, sv.BoxAnnotator):
                image = annotator.annotate(
                    image,
                    detections=self._filter_controller(
                        self.state["detections_stack"][-1]
                    ),
                    labels=self.state["last_classes"],
                )

            # convert to rgb
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.notebook:
            buffer = io.BytesIO()
            import base64

            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            # show image
            if annotator:
                fig = plt.figure(figsize=(8, 8))
                # if grey, show in grey
                if len(image.shape) == 2:
                    plt.imshow(image, cmap="gray")
                # if bgr, show in rgb
                elif image.shape[2] == 3:
                    plt.imshow(image[:, :, ::-1])

                fig.savefig(buffer, format="png")
                buffer.seek(0)

                image = Image.open(buffer)

                img_str = {"image": base64.b64encode(buffer.getvalue()).decode("utf-8")}

                self.state["output"] = {"image": img_str}

                return
            else:
                # if ndarray, convert to PIL
                if isinstance(image, np.ndarray):
                    image = Image.fromarray(image)
                    # do bgr to rgb
                    image = image.convert("RGB")

                # # convert to rgb if needed
                if image.mode != "RGB":
                    image = image.convert("RGB")

                # PIL to base64
                buffered = io.BytesIO()

                # save to either jpeg or png

                if self.state.get("last_loaded_image_name", "").endswith(".jpg"):
                    image.save(buffered, format="JPEG")
                else:
                    image.save(buffered, format="PNG")

                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            self.state["output"] = {"image": img_str}

            return

        if self.state.get("ctx", None) and self.state["ctx"].get("camera", None):
            self.state["image_stack"][-1] = image

            # show image

            # cv2.imshow("image", image)
        else:
            sv.plot_image(image, (8, 8))

    def get_func(self, x):
        self.state["last"] = self.state["last"][x]

    def similarity(self, n):
        """
        Get similarity of last N images.
        """
        if not n:
            n = 2

        if len(self.state["image_stack"]) < 2 or len(self.state["image_stack"]) < n:
            print("Not enough images to compare.")
            return

        import clip

        model, preprocess = clip.load("ViT-B/32", device=DEVICE)

        images = []

        for image in self.state["image_stack"][-n:]:
            image = preprocess(Image.fromarray(image)).unsqueeze(0).to(DEVICE)
            images.append(image)

        embeddings = []

        with torch.no_grad():
            for image in images:
                image = model.encode_image(image)

                embeddings.append(image)

        # get similarity
        similarity = torch.cosine_similarity(embeddings[0], embeddings[1])

        # cast tensor to float
        as_float = similarity.item()

        self.state["last"] = as_float

        return as_float

    def read_qr(self, _):
        """
        Read QR code from last image.
        """
        image = self._get_item(-1, "image_stack")

        data, _, _ = cv2.QRCodeDetector().detectAndDecode(image)

        return data

    def set_brightness(self, brightness):
        """
        Set brightness of last image.
        """
        # brightness is between -100 and 100
        image = self._get_item(-1, "image_stack")

        # use cv2
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # add brightness
        lim = 255 - brightness

        v[v > lim] = 255
        v[v <= lim] += brightness

        final_hsv = cv2.merge((h, s, v))

        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        self._add_to_stack("image_stack", image)
        self.state["output"] = {"image": image}

    def contains(self, statement):
        """
        Check if a statement is contained in the last statement.
        """
        if isinstance(self.state["last"], str):
            return statement in self.state["last"]
        else:
            return False

    def check_inputs(self, tree):
        # get all INPUT tokens and save them to state
        for node in tree.children:
            # if node has children, recurse
            if hasattr(node, "children") and len(node.children) > 0:
                self.check_inputs(node)

            if not hasattr(node, "data"):
                continue

            if node.data == "input":
                self.state["input_variables"][node.children[0].value] = "image"

    def parse_tree(self, tree):
        try:
            self.evaluate_tree(tree)
        except MemoryError:
            print("The program has ran out of memory.")
            exit()

    def evaluate_tree(self, tree):
        """
        Abstract Syntax Tree (AST) parser for VisionScript.
        """

        if not hasattr(tree, "children"):
            if hasattr(tree, "value") and tree.value.isdigit():
                return int(tree.value)
            elif isinstance(tree, str):
                return literal_eval(tree)
            elif hasattr(tree, "value") and tree.value.isfloat():
                return float(tree.value)

        if hasattr(tree, "children") and tree.data == "input":
            return self.input_(tree.children[0].value)

        for node in tree.children:
            print(node)
            if node == "True":
                return True
            elif node == "False":
                return False
            # if equality, check if equal
            # if rule is input
            elif hasattr(node, "data") and node.data == "equality":
                return self.parse_tree(node.children[0]) == self.parse_tree(
                    node.children[1]
                )
            elif node is True or node is False:
                return node
            elif hasattr(node, "data") and node.data == "list":
                node = node
            elif (hasattr(node, "type") and node.type == "INT") or isinstance(
                node, int
            ):
                return int(node.value)
            elif (hasattr(node, "type") and node.type == "FLOAT") or isinstance(
                node, float
            ):
                return float(node.value)
            elif not hasattr(node, "children") or len(node.children) == 0:
                node = node
            elif self.state.get("ctx") and (
                self.state["ctx"].get("in") or self.state["ctx"].get("if")
            ):
                node = node
            # if string
            # elif len(node.children) == 1 and hasattr(node.children[0], "value"):
            #     return node.children[0].value
            # else:
            #     node = node.children

            # remove \n
            if hasattr(node, "value") and node.value == "\n":
                continue

            token = node.data if hasattr(node, "data") else node

            if token.value in aliased_functions:
                token.value = map_alias_to_underlying_function(token.value)

            if token.type == "equality":
                return self.parse_tree(node.children[0]) == self.parse_tree(
                    node.children[1]
                )
            
            if token == "break":
                self.state["ctx"]["break"] = True
                return

            if token == "comment":
                continue

            if token == "expr":
                self.parse_tree(node)
                continue

            if token.type == "BOOL":
                return node.children[0].value == "True"

            if token == "list":
                results = []

                for item in node.children:
                    results.append(self.parse_tree(item))

                return results

            if token == "var":
                self.state[node.children[0].children[0].value] = self.parse_tree(
                    node.children[1]
                )
                self.state["last"] = self.state[node.children[0].children[0].value]
                continue

            if token.value == "if":
                # copy self.state
                if not cv2.VideoCapture(0).isOpened():
                    last_state_before_if = copy.deepcopy(self.state)["last"]

                if self.state.get("ctx"):
                    self.state["ctx"]["if"] = True
                else:
                    self.state["ctx"] = {"if": True}

                # if equality, check if equal

                statement = self.parse_tree(node.children[0])

                statement = self.state["last"]

                if statement is None or statement == False or int(statement) == 0:
                    return

                # if not cv2.VideoCapture(0).isOpened():
                #     self.state["last"] = last_state_before_if

            if token.value == "make":
                self.make(node.children)
                continue

            if token.value == None:
                continue

            # if gt, lt, gte, lte, etc, call with x as first arg and y as second arg
            if token.value in ["gt", "lt", "gte", "lte"]:
                result1 = self.parse_tree(node.children[0])
                result1 = self.state["last"] if result1 is None else result1
                result2 = self.parse_tree(node.children[1])
                result2 = self.state["last"] if result2 is None else result2
                return self.function_calls[token.value]([result1, result2])

            if token.value == "literal":
                func = self.state["functions"][node.children[0].value]
            else:
                func = self.function_calls[token.value]

            if token.value == "negate" or token.value == "input":
                result = self.parse_tree(node.children[0])
                return func(result)

            if token.value == "get":
                get_value = self.parse_tree(node.children[0])

                if get_value is None and self.state.get("get"):
                    del self.state["get"]
                else:
                    self.state["get"] = get_value
                continue

            self.state["history"].append(token.value)

            # if token.value == "say":
            #     value = self.state["last"]
            #     func(value)
            #     continue
            if token.value == "contains":
                return func(literal_eval(node.children[0]))
            else:
                # convert children to strings
                for item in node.children:
                    if hasattr(item, "value"):
                        if item.value.startswith('"') and item.value.endswith('"'):
                            item.value = literal_eval(item.value)
                        elif item.type in ("EOL", "INDENT", "DEDENT"):
                            continue
                        elif item.type == "STRING":
                            item.value = literal_eval(item.value)
                        elif item.type == "INT":
                            item.value = int(item.value)
                        elif item.type == "input":
                            item.value = self.parse_tree(item.value)
                        elif item.type == "FLOAT":
                            item.value = float(item.value)

            if token.value == "in" or token.value == "usecamera":
                # if file_name == "camera", load camera in context
                # if node.children[0].value is an expr, evaluate it
                # evaluate all children

                if token.value == "usecamera":
                    self.state["ctx"]["fps"] = 0
                    self.state["ctx"]["active_file"] = None
                    self.state["ctx"]["camera"] = cv2.VideoCapture(0)

                    context = node.children[2:]

                    start_time = time.time()
                    counter = 0

                    # exit()

                    while True:
                        frame = self.state["ctx"]["camera"].read()[1]

                        self.state["ctx"]["active_file"] = frame
                        self._add_to_stack("image_stack", frame)

                        for item in context:
                            # add to image
                            # if ctx break, break
                            if self.state["ctx"].get("break"):
                                self.state["ctx"]["break"] = False
                                break

                            self.parse_tree(item)

                        cv2.imshow("frame", self._get_item(-1, "image_stack"))
                        cv2.waitKey(1)

                        counter += 1

                        self.state["ctx"]["fps"] = round(
                            counter / (time.time() - start_time)
                        )

                        counter = 0
                        start_time = time.time()

                elif hasattr(node.children[0], "value") and isinstance(
                    node.children[0].value, str
                ):
                    self.state["ctx"]["in"] = os.listdir(node.children[0].value)
                # if expression, eval
                elif hasattr(node.children[0], "value"):
                    self.state["ctx"]["in"] = self.parse_tree(node.children[0])

                for item in node.children:
                    if self.state["ctx"].get("break"):
                        self.state["ctx"]["break"] = False
                        break

                    self.parse_tree(item)

                for file_name in self.state["ctx"].get("in", []):
                    # must be image
                    if not file_name.endswith(
                        (".jpg", ".png", ".jpeg", ".mov", ".mp4")
                    ):
                        continue

                    if file_name.endswith((".mov", "mp4")):
                        video_info = sv.VideoInfo.from_video_path(video_path=file_name)

                        self.state["ctx"]["video_events_from_Classify[]"] = []
                        self.state["ctx"]["current_frame_count"] = 0
                        self.state["ctx"]["fps"] = video_info.fps

                        with sv.VideoSink(
                            target_path="result.mp4", video_info=video_info
                        ) as sink:
                            # make this concurrent if in fast context

                            for i, frame in enumerate(sv.get_video_frames_generator(
                                source_path="source_video.mp4", stride=VIDEO_STRIDE
                            )):
                                self.state["ctx"]["current_frame_count"] = i

                                # ignore first three items, which don't contain instructions
                                context = node.children[3:]

                                for item in context:
                                    if self.state["ctx"].get("break"):
                                        self.state["ctx"]["break"] = False
                                        break
                                    self.state["ctx"]["active_file"] = frame
                                    self.parse_tree(item)
                                    sink.write_frame(self.state["last"])
                    else:
                        self.state["ctx"]["active_file"] = os.path.join(
                            literal_eval(node.children[0]), file_name
                        )

                        # ignore first 2, then do rest
                        context = node.children[3:]

                        for item in context:
                            if self.state["ctx"].get("break"):
                                self.state["ctx"]["break"] = False
                                break
                            self.parse_tree(item)

                if self.state["ctx"].get("in"):
                    del self.state["ctx"]["in"]
                    del self.state["ctx"]["active_file"]

                # set concurrent context to false
                self.state["in_concurrent_context"] = False

                continue

            if len(node.children) == 1:
                if hasattr(node.children[0], "value"):
                    value = node.children[0].value
                else:
                    value = self.parse_tree(node.children[0])
            elif all([hasattr(item, "value") for item in node.children]):
                value = [item.value for item in node.children]
            else:
                value = [self.parse_tree(item) for item in node.children]

            if token.value == "literal":
                result = self.parse_tree(self.state["functions"][value])
            else:
                result = func(value)

            # print("just run", token.value, "with", value, "returning result", result)

            self.state["last_function_type"] = token.value
            self.state["last_function_args"] = [value]

            if token.value == "load":
                self._add_to_stack("load_queue", result[0])
                continue

            if result is not None:
                self.state["last"] = result
                self.state["output"] = {"text": result}

            # return result


def activate_console(parser):
    print("Welcome to VisionScript!")
    print("Type 'Exit[]' to exit.")
    print("Read the docs at https://visionscript.org/docs")
    print("For help, type 'Help[FunctionName]'.")
    print("-" * 20)

    session = VisionScript()

    while True:
        code = input(">>> ")

        tree = None

        try:
            tree = parser.parse(code + "\n")  # .lstrip())
        except UnexpectedCharacters as e:
            handle_unexpected_characters(e, code + "\n", interactive=True)  # .lstrip())
        except UnexpectedToken as e:
            handle_unexpected_token(e, interactive=True)
        finally:
            if tree is None:
                continue

        session.parse_tree(tree)


@click.command()
@click.option("--validate", default=False, help="")
@click.option("--ref", default=False, help="Name of the file")
@click.option("--debug", default=False, help="To debug")
@click.option("--file", default=None, help="Name of the file")
@click.option("--repl", default=None, help="To enter to visionscript console")
@click.option("--notebook/--no-notebook", help="Start a notebook environment")
@click.option("--cloud/--no-cloud", help="Start a cloud deployment environment")
@click.option("--deploy", help="Deploy a .vic file", default=None)
@click.option(
    "--name",
    help="Application name (used if you are deploying your app via --deploy)",
    default=None,
)
@click.option(
    "--description",
    help="Application description (used if you are deploying your app via --deploy)",
    default=None,
)
@click.option("--api-key", help="API key for deploying your app", default=None)
@click.option(
    "--api-url",
    help="API url for deploying your app",
    default="http://localhost:6999/create",
)
@click.option("--live", help="Live mode", default=False)
def main(
    validate,
    ref,
    debug,
    file,
    repl,
    notebook,
    cloud,
    deploy,
    name,
    description,
    api_key,
    api_url,
    live,
) -> None:
    if validate:
        print("Script is a valid VisionScript program.")
        exit(0)

    if ref:
        print(USAGE.strip())

    if notebook:
        print("Starting notebook...")
        import webbrowser

        from visionscript.notebook import app

        # webbrowser.open("http://localhost:5001/notebook?" + str(uuid.uuid4()))

        app.run(debug=True, host="0.0.0.0", port=5001, ssl_context="adhoc")

        return

    if cloud:
        print("Starting cloud deployment environment...")

        from visionscript.cloud import app

        app.run(debug=True, port=6999)

    if file is not None:
        with open(file, "r") as f:
            code = f.read() + "\n"

        tree = parser.parse(code.lstrip())

        if debug:
            print(tree.pretty())
            exit()

        session = VisionScript()

        if deploy:
            if not name or not description or not api_key or not api_url:
                print("Please provide a name, description, api key, and api url.")
                return

            session.notebook = True

            session.check_inputs(code)

            import requests

            app_slug = name.translate(
                str.maketrans("", "", string.punctuation.replace("-", ""))
            ).replace(" ", "-")

            deploy_request = requests.post(
                api_url,
                json={
                    "title": name,
                    "slug": app_slug,
                    "api_key": api_key,
                    "description": description,
                    "script": code,
                    "variables": session.state["input_variables"],
                },
            )

            if deploy_request.ok:
                print("App deployed to", deploy_request.json()["url"])

            return

        if live:
            session.parse_tree(tree)

            observer = Observer()

            event_handler = watchdog.events.FileSystemEventHandler()

            # when file changes, run code
            def on_modified(event):
                if event.src_path == os.path.abspath(file):
                    print("Running code...")
                    tree = parser.parse(code.lstrip())

                    session.parse_tree(tree)

            event_handler.on_modified = on_modified

            observer.schedule(
                event_handler,
                os.path.dirname(os.path.abspath(file)),
                recursive=True,
            )

            observer.start()

            try:
                while True:
                    time.sleep(1)
            finally:
                observer.stop()
                observer.join()

                exit()

        session.parse_tree(tree)

    if repl == "console":
        activate_console(parser)


if __name__ == "__main__":
    main()
