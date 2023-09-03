import re
import base64
import fire
from loguru import logger

# 参考链接：https://subce.gitee.io/htmls/essays/typora_base64_html.html

OFFLINE_IMG_PATTERN = r'^.*!\[.*\]\((.*\.[a-z]*)\).*$'
ONLINE_IMG_PATTERN = r'^.*<img src="(.*\.[a-z]*)" ([a-z]*=.*;)" />.*$'

class Typora(object):
    """
    将 typora 的图片嵌入 markdown 里面的代码

    Usage:
        python typora.py main
    """
    def __init__(self):
        pass

    def online_img2base64(self, md_dir, line_match, image_num, image_base64_list, line_front, line_after):
        image_path = md_dir + line_match.group(1)
        # image_path = line_match.group(1)
        _, image_num = self.offline_img2base64(line_match, image_num, image_base64_list)
        new_line_content = f"{line_front}![][{image_num}]{line_after}"
        return new_line_content, image_num

    def offline_img2base64(self, line_match, image_num, image_base64_list):
        image_name = line_match.group(1)
        image_num = image_num + 1
        try:
            with open(image_name, 'rb') as photograph:
                image_binary_data = photograph.read()
                image_base64_data = str(base64.b64encode(image_binary_data), encoding='utf-8')
        except:
            image_base64_data = f"{image_name} is not exist"
        image_name = image_name.split('\\')[-1]
        image_type = image_name.split('.')[-1].lower()
        logger.debug(f"The {image_num} image is {image_name}, and the type is {image_type}")
        image_base64_list.append({image_type: image_base64_data})
        new_line_content = f"![{image_name}][{image_num}]"
        logger.debug(f"new_line_content: {new_line_content}")
        return new_line_content, image_num

    def base642image(self, md_name, image_base64_list, image_path):
        """
        将 base64 编码转换为图片
        """
        image_data = base64.b64decode(image_base64_list)
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
    def images2base64(self, md_dir, md_name):
        typora_md_name = f"{md_dir}{md_name}.md"
        typora_md_new_name = f"{md_dir}{md_name}_html.md"

        image_base64_list = [] # [{key: base64_type, value: base64_data}]
        image_num = 0

        offline_compile = re.compile(OFFLINE_IMG_PATTERN, flags=re.MULTILINE)
        online_compile = re.compile(ONLINE_IMG_PATTERN, flags=re.MULTILINE)

        with open(typora_md_name, 'r', encoding='utf-8') as f1, open(typora_md_new_name, 'w', encoding='utf-8') as f2:
            logger.info(f"Start to convert {typora_md_name} to {typora_md_new_name}")
            for line_content in f1.readlines():
                # for regular in [offline_compile, online_compile]:
                offline_match = offline_compile.match(line_content)
                online_match = online_compile.match(line_content)
                
                if offline_match:
                    new_line_content, image_num = self.offline_img2base64(offline_match, image_num, image_base64_list)
                elif online_match:
                    line_front = line_content[0:online_match.regs[1][0]][:-10]
                    line_after = line_content[online_match.regs[2][1]:]
                    new_line_content, image_num = self.online_img2base64(md_dir, online_match, image_num, image_base64_list, line_front, line_after)
                else:
                    new_line_content = line_content
                f2.write(new_line_content)

            f2.write("\n\n")
            logger.info(f"Starting to write base64 data to {typora_md_new_name}")
            for index, base64_dict in enumerate(image_base64_list):
                base64_type, base64_data = next(iter(base64_dict.items()))
                # f2.write(f"<img src=\"data:image/{base64_type};base64,{base64_data}\n") # base64_type svg
                f2.write(f"[{index + 1}] \"data:image/{base64_type};base64,{base64_data}\n") # base64_type svg
            logger.info(f"Convert {typora_md_name} to {typora_md_new_name} successfully")

    def main(self):
        typora_md_dir = "./" # typora 绝对路径
        md_dir = "./" # md 文件夹 相对路径
        md_name = "test"
        self.images2base64(md_dir, md_name)

if __name__ == "__main__":
    fire.Fire(Typora)