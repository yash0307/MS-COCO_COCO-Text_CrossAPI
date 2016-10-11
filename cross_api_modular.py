### git @ yash0307 ###
import json
class CrossAPI(object):
	def __init__(self, mscoco, coco_text, data_type, output_path):
		self.mscoco = mscoco
		self.coco_text = coco_text
		self.data_type = data_type
		self.output_path = output_path
	def generateCrossData(self):
		if self.data_type == "val":
			im_ids_txt = self.coco_text.getImgIds(imgIds = self.coco_text.val)
		elif self.data_type == "train":
			im_ids_txt = self.coco_text.getImgIds(imgIds = self.coco_text.train)
		else:
			print ("Error : Invalid data type")
		G_TEXT_CAP = {}
		counter_image = 0
		counter_word_instances = 0
		counter_caption_instances = 0
		images_without_text = 0
		for i in im_ids_txt:
			counter_image += 1
			words_present = []
			ann_ids_txt = self.coco_text.getAnnIds(imgIds = i)
			ann_txt = self.coco_text.loadAnns(ann_ids_txt)
			for j in ann_txt:
				try:
					if j['utf8_string'] != '':
						counter_word_instances += 1
						words_present.append(j['utf8_string'])
				except KeyError:
					pass
			captions = []
			ann_ids_coco = self.mscoco.getAnnIds(imgIds = i)
			ann_coco = self.mscoco.loadAnns(ann_ids_coco)
			for j in ann_coco:
				try:
					if j['caption'] != '':
						counter_caption_instances += 1
						captions.append(str(j['caption']))
				except KeyError:
					pass
			if not words_present:
				 images_without_text += 1
			try:
				im = self.mscoco.loadImgs(i)
			except KeyError:
				print ("Error : Please specify data type for ms-coco as train")
			temp_dict = {}
			temp_dict['captions'] = captions
			temp_dict['text'] = words_present
			temp_dict['file_name'] = im[0]['file_name']
			G_TEXT_CAP[i] = temp_dict
		try:
			with open(self.output_path, "w") as fp:
				json.dump(G_TEXT_CAP, fp)
		except IOError:
			print ("Error : Invalid output file")
		print "Total number of images : " + str(counter_image)
		print "Total number of words : " + str(counter_word_instances)
		print "Total number of captions : " + str(counter_caption_instances)
		print "Total number of Images without Text : " + str(images_without_text)
