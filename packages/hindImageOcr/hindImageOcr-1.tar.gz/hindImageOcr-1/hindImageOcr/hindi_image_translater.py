import easyocr
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
import traceback

class HindiToEnglishTranslator:
    def __init__(self):
        self.reader = easyocr.Reader(['en', 'hi'])
        self.translator = Translator()
        self.hindi_number_map = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
    
    def __get_ocr_text_coordinates(self, input_path):
        result = self.reader.readtext(input_path)
        hindi_text = []
        bbox_coordinates = []
        for res in result:
            bbox_coordinates.append(tuple(res[0]))
            hindi_text.append(res[1])
        return hindi_text, bbox_coordinates
    
    def __translate_hindi_to_english(self, text):
        translated = self.translator.translate(text[1], src='hi', dest='en')
        return (text[0],translated.text)
    
    def __convert_hindi_numbers_to_english(self, text):
        for hindi_num, eng_num in self.hindi_number_map.items():
            text = text.replace(hindi_num, eng_num)
        return text
    
    def process_image(self, input_file_path):
        hindi_text, bbox_coordinates = self.__get_ocr_text_coordinates(input_file_path)

        processed_h_text = []
        for h_text in hindi_text:
            out = self.__convert_hindi_numbers_to_english(h_text,)
            processed_h_text.append(out)
            
        dataset_ = [[bbox,txt] for bbox,txt in zip(bbox_coordinates,processed_h_text)]

        translated_data = []
        for txt in dataset_:
            out = self.__translate_hindi_to_english(txt)
            translated_data.append(out)
        # with ThreadPoolExecutor(max_workers=20) as executor:
        #     translated_data = list(executor.map(self.__translate_hindi_to_english, dataset_))
        

        source_image = Image.open(input_file_path)
        draw_source = ImageDraw.Draw(source_image)

        for bbox, _ in translated_data:
            try:
                int_coordinates = [(int(x), int(y)) for x, y in bbox]
                draw_source.polygon(int_coordinates, outline=None, fill=(255, 255, 255))
            except:
                traceback.print_exc()

        new_image = Image.new('RGBA', source_image.size, (255, 255, 255, 255))
        new_image.paste(source_image, (0, 0))

        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 40)

        for bbox, english_text in translated_data:
            try:
                draw.polygon([tuple(point) for point in bbox], outline=False, width=0)
                draw.text(bbox[0], english_text, font=font, fill="black")
            except:
                traceback.print_exc()
        
        return new_image



