pip3 install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn >init.log 2>&1


if not exist venv (
    virtualenv venv
)

call .\venv\Scripts\activate >init.log 2>&1

pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn >init.log 2>&1