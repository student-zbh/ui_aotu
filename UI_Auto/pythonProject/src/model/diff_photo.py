import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim



class Diff_photo():

    def resize_images(self, image1, image2):
        """
        将两张图片统一大小
        """
        # 获取小的尺寸，以进行resize
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]
        height = min(h1, h2)
        width = min(w1, w2)

        # 调整大小
        resized_image1 = cv2.resize(image1, (width, height), interpolation=cv2.INTER_AREA)
        resized_image2 = cv2.resize(image2, (width, height), interpolation=cv2.INTER_AREA)

        return resized_image1, resized_image2

    def image_diff(self, image_path1, image_path2, diff_output_path):
        # 读取图片
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        # 检查图片是否加载成功
        if image1 is None:
            print(f"Error: Unable to load image from {image_path1}")
            return
        if image2 is None:
            print(f"Error: Unable to load image from {image_path2}")
            return

        # 调整图片大小
        image1, image2 = self.resize_images(image1, image2)

        # 确定 win_size
        min_dim = min(image1.shape[:2])
        win_size = min(7, min_dim) if min_dim >= 7 else 3  # 确保 win_size 不超过较小维度，并为一个奇数

        # 计算图片的SSIM
        sim_index, _ = ssim(image1, image2, channel_axis=-1, win_size=win_size, full=True)
        print(f"SSIM: {sim_index:.4f}")

        # 计算图片差异
        diff = cv2.absdiff(image1, image2)

        # 将差异转换为灰度图
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # 提取差异区域
        _, threshold_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

        # 寻找轮廓
        contours, _ = cv2.findContours(threshold_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 在原图上绘制不同区域
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # 忽略小差异
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # 保存diff结果
        cv2.imwrite(diff_output_path, image1)

        # 显示diff结果
        cv2.imshow('Differences', image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def template_match(self, base_photo_path, test_photo_path, threshold=0.8):

        """
        检测大图中是否包含某个元素。

        :param main_image_path: 大图路径
        :param template_image_path: 小图（模板）路径
        :param threshold: 匹配度阈值（0到1之间）
        :return: 返回匹配的坐标，如果找到了匹配则返回True，否则返回False
        """
        # 读取大图和小图
        main_image = cv2.imread(base_photo_path)
        template_image = cv2.imread(test_photo_path)

        # 检查是否成功加载图片
        if main_image is None:
            print(f"Error: Unable to load main image from {base_photo_path}")
            return False
        if template_image is None:
            print(f"Error: Unable to load template image from {test_photo_path}")
            return False

        # 获取图像的宽和高
        main_height, main_width = main_image.shape[:2]
        template_height, template_width = template_image.shape[:2]

        # 检查模板是否大于主图
        if template_height > main_height or template_width > main_width:
            print("Error: Template image is larger than the main image.")
            return False

        # 执行模板匹配
        result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)

        # 获取匹配结果中大于阈值的位置
        locations = np.where(result >= threshold)

        # 遍历找到的位置并在大图上画出匹配区域
        found = False
        for pt in zip(*locations[::-1]):  # `locations` 是先行后列因此此处需反序
            found = True
            cv2.rectangle(main_image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 255, 0), 2)

        # 显示结果
        cv2.imshow("Matched Result", main_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return found