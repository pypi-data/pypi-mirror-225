import cv2
import numpy as np
from pyzjr.ColorModule import ColorFinder
from pyzjr.Showimage import StackedImages

class getMask():
    def __init__(self, trackBar=True):
        self.ColF = ColorFinder(trackBar)
        # self.ColF.initTrackbars()
    def protect_region(self, mask ,threshold=None):
        """
        * 用于保护掩膜图的部分区域
        :param mask: 掩膜图
        :param threshold: 如果为None,则为不保护，如果是长为4的列表，则进行特定区域的保护
        :return: 返回进行保护区域的掩膜图

        example:    [0, img.shape[1], 0, img.shape[0]]为全保护状态，
                    x_start可以保护大于x的部分
                    x_end可以保护小于x的部分
                    y_start可以保护图像下方的部分
                    y_end可以保护图像上方的部分
        """
        if threshold == None:
            return mask
        else:
            x_start, x_end, y_start, y_end = threshold[:4]
            mask[y_start:y_end, x_start:x_end] = 0
            return mask

    def MaskZone(self, img, HsvVals):
        """
        * 生成掩膜图以及融合图像
        :param img: 输入图像
        :param HsvVals: 可以通过getTrackbarValues获得
        :return: 返回融合图、掩膜图、HSV图
        """
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array(HsvVals[0])
        upper = np.array(HsvVals[1])
        mask = cv2.inRange(imgHSV, lower, upper)
        imgResult = cv2.bitwise_and(img, img, mask=mask)
        return imgResult, mask

    def DetectImg(self, path, ConsoleOut=True, threshold=None, scale=1.0):
        """
        * 轨迹栏检测图片
        :param path: 图片路径
        :param ConsoleOut: 用于是否控制台打印HsvVals的值
        :param threshold: 阈值，用于保护图片的区域
        :param scale: 图片规模大小
        :return: 无返回
        """
        while True:
            img = cv2.imread(path)
            HsvVals = self.ColF.getTrackbarValues(False)
            if ConsoleOut:
                print(HsvVals)
            imgResult, mask, imgHSV = self.MaskZone(img,HsvVals)
            pro_mask = self.protect_region(mask, threshold)
            imgStack = StackedImages(scale, ([img,imgHSV],[pro_mask,imgResult]))
            cv2.imshow("Stacked Images", imgStack)
            k = cv2.waitKey(1)
            if k == 27:
                break


if __name__=="__main__":
    path = r'ces\test\03.jpg'
    img2 = cv2.imread(path)
    getMask=getMask()
    getMask.DetectImg(path,threshold=[0, img2.shape[1], 300, img2.shape[0]],scale=0.4)





