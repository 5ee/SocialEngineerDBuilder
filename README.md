这是一个整理社工库的工具，定义了一套DSL语言，对于不同的格式只需要简单配置一行就可以自动化导入数据库，也支持整理成入库的SQL语句，从文件导入，速度更快，相对操作也较为繁琐。

———————————————————————
用法：
User.py 建表

模板：
分隔符: 支持常见字符如SPACE（空格）, | : 等，也可以自定义
数据行描述: 
支持的数据格式（详见User.py）
username 
username_zh 中文名字
passwd 明文密码
email
identify_number 身份证18位
cell_phone 手机号码
ip_addr ip地址
living_place 住址

数据格式描述示例
分隔符 数据描述（以'|'分割，ignore是需要忽略的数据项）
SPACE username|password|cell_phone|
, username|password|identify_number|ignore|ignore|email

如果希望丰富数据项，可以修改User.py中的model定义，即可自动支持。

示例用法：
模板内容
$ cat kuzi.tmpl
, username|password|ignore|ignore|cell_phone

数据格式
$ head kuzi.txt
user1,123456,nihao,10.0.1.1,13111110000
user2,123456,wtf,192.32.1.199,13111110001
...

python SG.py kuzi.txt kuzi.tmpl
唰～～