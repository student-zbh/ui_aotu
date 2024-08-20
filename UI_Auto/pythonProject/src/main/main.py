from src.model.diff_photo import Diff_photo
# 使用方法

image_path1 = '/Users/zhangbohan/UI_Auto/pythonProject/base_photo/1.png'
image_path2 = '/Users/zhangbohan/UI_Auto/pythonProject/test_photo/2.png'
diff_output_path = '/base_photo/1.png'
main_image_path = '/Users/zhangbohan/UI_Auto/pythonProject/base_photo/1.png'
template_image_path = '/Users/zhangbohan/UI_Auto/pythonProject/test_photo/2.png'

if __name__ == '__main__':
    diff = Diff_photo()
    diff.image_diff(image_path1=image_path1, image_path2=image_path2, diff_output_path=diff_output_path)
    # diff.template_match(image_path1,image_path2)