import kwcoco
dset = kwcoco.CocoDataset.demo('vidshapes8')


coco_img = dset.images().coco_images[0]


tmp = kwcoco.CocoDataset()

tmp.add_video(**coco_img.video)
tmp.add_image(**coco_img.img)
