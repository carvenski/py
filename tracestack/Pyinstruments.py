
# Pyinstruments��Python�ĵ���ջ������
# https://github.com/joerick/pyinstrument

'''
Pyinstruments����ƻ��InstrumentsӦ����������һ��Python����������¼��ִ�д���ĵ���ջ��
��ʹ��һ����̬����������ζ�Ŵ���������ԣ�1 ms���Ĵ�ջ��ȡ������Ȼ����¼��ķ���������Ҫ�͡�
'''


# �����ֱ�Ӵ������е���pyinstrument
python -m pyinstrument myscript.py [args...]


# ����
from pyinstrument import Profiler

profiler = Profiler() # or Profiler(use_signal=False), see below
profiler.start()

# --> ��Ҫ�����Ĵ����������

profiler.stop()

print(profiler.output_text(unicode=True, color=True))  































