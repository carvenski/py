
'''
���Ϸ��������ڱȽϼ򵥵ĳ��ϣ������ӵ�����£������ñ�׼�������profile����cProfile��������ͳ�Ƴ�����ÿһ������������ʱ�䣬�����ṩ�˿��ӻ��ı����������£�����ʹ��cProfile������profile��Cʵ�֣�����������ʱ�䳤�ĳ��򡣲����е�ϵͳ���ܲ�֧��cProfile����ʱֻ����profile��

���������������� timeit_profile() ��������ʱ����������

Python
'''

import cProfile
from time_profile import *

cProfile.run("timeit_profile()")

'''
������������ܻ�ܳ����ܶ�ʱ�����Ǹ���Ȥ�Ŀ���ֻ�к�ʱ���ļ������������ʱ���Ƚ�cProfile ��������浽����ļ��У�Ȼ���� pstats ���Ƹ����кõ���������������� gist �ϣ���

Python
'''

cProfile.run("timeit_profile()", "timeit")
p = pstats.Stats('timeit')
p.sort_stats('time')
p.print_stats(6)

