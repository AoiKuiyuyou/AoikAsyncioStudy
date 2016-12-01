[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikAsyncioStudy
Python **asyncio** library study.

Tested working with:
- Python 3.5

Trace call using [AoikTraceCall](https://github.com/AoiKuiyuyou/AoikTraceCall):
- [EchoProtocolTraceCall.py](/src/EchoProtocolTraceCall.py)
- [EchoProtocolTraceCallLogPy3.txt](/src/EchoProtocolTraceCallLogPy3.txt?raw=True)
- [EchoProtocolTraceCallNotesPy3.txt](/src/EchoProtocolTraceCallNotesPy3.txt?raw=True)

## Table of Contents
[:toc(beg='next', indent=-1)]

## Set up AoikTraceCall
[:tod()]

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikTraceCall
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikTraceCall

cd AoikTraceCall

python setup.py install
```

## Usage
[:tod()]

### Start server
Run:
```
python "AoikAsyncioStudy/src/EchoProtocolTraceCall.py" > Log.txt 2>&1
```

### Send request
Run:
```
echo hello| nc 127.0.0.1 8000
```
