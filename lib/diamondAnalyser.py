class DiamondAnalyser:
    def __init__(self, visual_gene, name, number):
        self.visual_gene = visual_gene
        self.name = name
        self.number = number
        # 默认为普通钻石
        self.shape = ""
        # color 异形才有
        self.color = ""
        self.styles = ""

        self.number_literal = ""
        self.name_literal = ""

        self.score = 0
        self.shape_features = []
        self.color_features = []
        self.style_features = []
        self.number_literal_features = []
        self.name_literal_features = []

    def analyse(self):
        # 分析形状
        shape = self.analyse_shape()
        self.shape = shape['shape']
        self.shape_features.extend(shape['features'])
        self.score += shape['score']

        if not self.shape:
            styles = self.analyse_styles()
            self.styles = styles['styles']
            self.score += styles['score']
            self.style_features.extend(styles['features'])
        else:
            # 异形
            color = self.analyse_color()
            self.color = color['color']
            self.score += color['score']
            self.color_features.extend(color['features'])

        number_literal = self.analyse_number_literal()
        self.number_literal = number_literal['number_literal']
        self.number_literal_features.extend(number_literal['features'])
        self.score += number_literal['score']

        name_literal = self.analyse_name_literal()
        self.name_literal = name_literal['name_literal']
        self.name_literal_features.extend(name_literal['features'])
        self.score += name_literal['score']

    def analyse_shape(self):
        # 获取前两位作为形状代码
        shape_code = self.visual_gene[:2]

        # 形状映射表
        shape_map = {
            "01": {"name": "Square", "score": 30},      # 长方形
            "02": {"name": "Ellipse", "score": 30},     # 椭圆
            "03": {"name": "Heart", "score": 50},       # 爱心
            "04": {"name": "Triangle", "score": 20},    # 三角
            "05": {"name": "Teardrop", "score": 30},    # 水滴
            "06": {"name": "Circle", "score": 30},      # 圆形
            "07": {"name": "Rhombus", "score": 20},     # 菱形
            "08": {"name": "Hexagon", "score": 20}      # 六边形
        }

        shape = ""
        features = []
        score = 0

        # 查找对应的形状
        shape_info = shape_map.get(shape_code)

        if shape_info:
            shape = f"{shape_info['name']}|{shape_code}"
            features.append(shape)
            score = shape_info['score']

        return {
            "shape": shape,
            "features": features,
            "score": score
        }

    @staticmethod
    def distinct_char(s):
        return len(set(s))

    @staticmethod
    def is_sequential(s, step):
        for i in range(len(s) - 1):
            if int(s[i + 1]) - int(s[i]) != step:
                return False
        return True

    @staticmethod
    def get_max_repeat_count(s):
        max_count = 1
        current_count = 1

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 1
        return max_count

    def analyse_color_type(self, style):
        dark_colors = set('01234')
        light_colors = set('56789abcdef')

        has_dark = False
        has_light = False

        for c in style.lower():
            if c in dark_colors:
                has_dark = True
            if c in light_colors:
                has_light = True
            if has_dark and has_light:
                return "mixed"

        if has_dark:
            return "dark"
        if has_light:
            return "light"
        return "mixed"

    def is_symmetric(self, s):
        mid = len(s) // 2
        first_half = s[:mid]
        second_half = ''.join(reversed(s[-mid:]))
        return first_half == second_half

    def analyse_color(self):
        style = self.visual_gene[2:19]
        name = self.name
        features = []

        # 颜色映射表
        color_map = {
            'A': {"name": "Red cyan", "score": 7},
            'B': {"name": "Cyan", "score": 6},
            'E': {"name": "Secret", "score": 1},
            'H': {"name": "Pink", "score": 8},
            'I': {"name": "Red", "score": 8},
            'K': {"name": "Pink cyan", "score": 8},
            'M': {"name": "Yellow secret", "score": 2},
            'N': {"name": "Yellow Cyan", "score": 6},
            'S': {"name": "Green", "score": 6},
            'T': {"name": "Blue", "score": 8},
            'U': {"name": "Blue purple", "score": 3},
            'V': {"name": "Light pink", "score": 8},
            'W': {"name": "Dark blue", "score": 3},
            'X': {"name": "Grey", "score": 5},
            'Y': {"name": "Red purple", "score": 3},
            'Z': {"name": "Gold", "score": 10}
        }

        # 根据名字首字母判断颜色
        first_char = name[0]
        if first_char in color_map:
            features.append(f"{color_map[first_char]['name']}|{first_char}")

        # 深浅色判断
        color_type = self.analyse_color_type(style)
        if color_type == "dark":
            features.append("darkColor|color")
        elif color_type == "light":
            features.append("lightColor|color")

        # 获取最高分的特征
        max_score = 0
        selected_feature = ""

        for feature in features:
            name, type_ = feature.split('|')
            score = 20 if type_ == 'color' else color_map.get(type_, {}).get('score', 0)

            if score > max_score:
                max_score = score
                selected_feature = name

        return {
            "color": selected_feature,
            "features": features,
            "score": max_score
        }

    def analyse_styles(self):
        style = self.visual_gene[2:18]
        thirteen, fourteen, fifteen, sixteen = style[12], style[13], style[14], style[15]

        # 样式映射表
        style_map = {
            "Pure": {"metric": "纯钻", "score": 250},
            "All 16 color": {"metric": "十六色", "score": 200},
            "All 15 color": {"metric": "十五色", "score": 100},
            "All 14 color": {"metric": "十四色", "score": 30},
            "Sum seven color": {"metric": "七色", "score": 20},
            "Sum six color": {"metric": "六色", "score": 50},
            "Sum five color": {"metric": "五色", "score": 100},
            "Sum four color": {"metric": "四色", "score": 200},
            "darkColor": {"metric": "全深色系", "score": 20},
            "lightColor": {"metric": "全浅色系", "score": 20},
            "Double mix": {"metric": "双色混合", "score": 20},
            "Center color": {"metric": "中间两块同色", "score": 3},
            "Edge color": {"metric": "两边同色", "score": 3},
            "Half divide": {"metric": "两边各一半", "score": 20},
            "Left three pure": {"metric": "左三连", "score": 20},
            "Right three pure": {"metric": "右三连", "score": 20},
            "Left mix pure": {"metric": "左三混合", "score": 20},
            "Right mix pure": {"metric": "右三混合", "score": 20},
            "Color Symmetry": {"metric": "轴对称", "score": 20}
        }

        features = []

        # 纯色判断
        if thirteen == fourteen == fifteen == sixteen:
            features.append("Pure")
        # 左三连判断
        elif fourteen == fifteen == thirteen and fourteen != sixteen:
            features.append("Left three pure")
        # 左三混合判断
        elif thirteen == fifteen == sixteen and fourteen != thirteen:
            features.append("Left mix pure")
        # 右三连判断
        elif thirteen == fourteen == sixteen and fifteen != thirteen:
            features.append("Right three pure")
        # 右三混合判断
        elif fourteen == sixteen == fifteen and fourteen != thirteen:
            features.append("Right mix pure")
        # 对称性判断
        elif sixteen == fifteen and thirteen == fourteen:
            features.append("Color Symmetry")
        # 对半分判断
        elif sixteen == fourteen and thirteen == fifteen:
            features.append("Half divide")
        # 双色混合判断
        elif (fifteen + thirteen) == (fourteen + sixteen):
            features.append("Double mix")
        # 中心颜色判断
        elif thirteen == fourteen and fifteen != sixteen:
            features.append("Center color")
        # 边缘颜色判断
        elif fifteen == sixteen and fourteen != thirteen:
            features.append("Edge color")

        # 颜色数量判断
        distinct_colors = self.distinct_char(style)
        if distinct_colors == 4:
            features.append("Sum four color")
        elif distinct_colors == 5:
            features.append("Sum five color")
        elif distinct_colors == 6:
            features.append("Sum six color")
        elif distinct_colors == 7:
            features.append("Sum seven color")
        elif distinct_colors == 14:
            features.append("All 14 color")
        elif distinct_colors == 15:
            features.append("All 15 color")
        elif distinct_colors == 16:
            features.append("All 16 color")

        # 深浅色判断
        color_type = self.analyse_color_type(style)
        if color_type == "dark":
            features.append("darkColor")
        elif color_type == "light":
            features.append("lightColor")

        # 获取最高分的特征
        max_score = 0
        selected_style = ""

        for feature in features:
            score = style_map[feature]["score"]
            if score > max_score:
                max_score = score
                selected_style = feature

        return {
            "styles": selected_style,
            "features": features,
            "score": max_score
        }

    def analyse_number_literal(self):
        number = self.number
        features = []

        # 规则映射表
        number_map = {
            "Single num": {"metric": "编号个位数", "score": 30},
            "Serial num": {"metric": "编号顺子", "score": 25},
            "Repetition": {"metric": "编号数字一样", "score": 50},
            "Number Symmetry": {"metric": "编号对称", "score": 10},
            "Tail four": {"metric": "编号4连", "score": 20},
            "Tail five": {"metric": "编号5连", "score": 50},
            "Tail six": {"metric": "编号6连", "score": 100},
            "Tail seven": {"metric": "编号7连", "score": 200}
        }

        # 个位数判断
        if int(number) < 10:
            features.append("Single num")

        # 数字全部相同
        if self.distinct_char(number) == 1:
            features.append("Repetition")

        # 顺子判断（递增或递减）
        if self.is_sequential(number, 1) or self.is_sequential(number, -1):
            features.append("Serial num")

        # 编号对称
        if self.is_symmetric(number):
            features.append("Number Symmetry")

        # 连续重复数字判断
        repeat_count = self.get_max_repeat_count(number)
        if repeat_count >= 4:
            if repeat_count == 7:
                features.append("Tail seven")
            elif repeat_count == 6:
                features.append("Tail six")
            elif repeat_count == 5:
                features.append("Tail five")
            elif repeat_count == 4:
                features.append("Tail four")

        # 获取最高分的特征
        max_score = 0
        selected_feature = ""

        for feature in features:
            score = number_map[feature]["score"]
            if score > max_score:
                max_score = score
                selected_feature = feature

        return {
            "number_literal": selected_feature,
            "features": features,
            "score": max_score
        }

    def analyse_name_literal(self):
        name = self.name
        features = []

        # 规则映射表
        name_map = {
            "Two letters": {"metric": "两种字母", "score": 10},
            "Three letters": {"metric": "三种字母", "score": 3},
            "Triple repeat": {"metric": "三字母重复", "score": 2},
            "Quadro repeat": {"metric": "四字母重复", "score": 10},
            "Penta repeat": {"metric": "五字母重复", "score": 50},
            "six repeat": {"metric": "六字母重复", "score": 200},
            "Symmetric letter": {"metric": "字母对称", "score": 10},
            "ABCABC": {"metric": "ABCABC类型", "score": 20},
            "ABBCDD": {"metric": "ABBCDD类型", "score": 10},
            "AABCCD": {"metric": "AABCCD类型", "score": 10}
        }

        # 连续重复字母判断
        repeat_count = self.get_max_repeat_count(name)
        if repeat_count >= 3:
            if repeat_count == 6:
                features.append("six repeat")
            elif repeat_count == 5:
                features.append("Penta repeat")
            elif repeat_count == 4:
                features.append("Quadro repeat")
            elif repeat_count == 3:
                features.append("Triple repeat")

        # 不同字母数量判断
        distinct_count = self.distinct_char(name)
        if distinct_count == 2:
            features.append("Two letters")
        elif distinct_count == 3:
            features.append("Three letters")

        # ABCABC类型
        if name[:3] == name[3:]:
            features.append("ABCABC")

        # 对称判断
        if self.is_symmetric(name):
            features.append("Symmetric letter")

        # AABCCD模式判断
        if name[0] == name[1] and name[3] == name[4]:
            features.append("AABCCD")

        # ABBCDD模式判断
        if name[1] == name[2] and name[4] == name[5]:
            features.append("ABBCDD")

        # 获取最高分的特征
        max_score = 0
        selected_feature = ""

        for feature in features:
            score = name_map[feature]["score"]
            if score > max_score:
                max_score = score
                selected_feature = feature

        return {
            "name_literal": selected_feature,
            "features": features,
            "score": max_score
        }

    @property
    def features(self):
        # 获取所有特征
        return (self.shape_features + 
                self.color_features + 
                self.style_features + 
                self.number_literal_features + 
                self.name_literal_features) 