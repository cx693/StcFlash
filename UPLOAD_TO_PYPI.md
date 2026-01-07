# 上传 stcflash 到 PyPI 官方仓库

## ✅ 当前状态

- **构建状态**：✅ 完成
- **包验证**：✅ 通过 (twine check PASSED)
- **包文件**：
  - `dist/stcflash-0.10.tar.gz` (源代码分发)
  - `dist/stcflash-0.10-py3-none-any.whl` (wheel 包)

## 前置要求

### 1. 工具安装 (已完成)
```bash
pip install twine wheel
```

### 2. PyPI 官方账户
- 访问 https://pypi.org/account/register/
- 填写用户名、邮箱、密码
- 验证邮箱

### 3. 创建 PyPI API token（推荐方式）
- 登录 PyPI 账户：https://pypi.org/manage/account/
- 在左侧菜单点击 "API tokens"
- 点击 "Add API token"
- 输入 token 名称（例如：stcflash-upload）
- 选择 "Scope"：建议选择 "Entire account" 或仅针对 "stcflash" 项目
- 复制生成的 token（格式：`pypi-...`）

## 配置认证信息

### 方式 A：创建 .pypirc 文件（推荐）

在用户主目录创建 `~/.pypirc` 文件（Windows 用户在 `C:\Users\<你的用户名>\.pypirc`）：

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-你的token值
```

### 方式 B：命令行输入（每次上传时输入）

上传时会提示输入用户名和密码。

## 验证包信息

在上传前，检查包的元数据是否正确：

```bash
cd c:\Users\CXi\Desktop\stcgal-master
twine check dist/stcflash-0.10.tar.gz dist/stcflash-0.10-py3-none-any.whl
```

✅ **当前验证结果**：
```
Checking dist\stcflash-0.10-py3-none-any.whl: PASSED
Checking dist\stcflash-0.10.tar.gz: PASSED
```

包已准备就绪！

## ⭐ 快速上传指南

### 第一步：准备账户 (你需要手动完成)

1. 访问 https://pypi.org/account/register/
2. 或 登录已有账户：https://pypi.org/manage/account/
3. 点击上方菜单的 "API tokens"
4. 点击 "Add API token" 按针
5. 输入名称（例如：stcflash-release）
6. 复制生成的 token (会出现成 `pypi-...` 格式)

### 第二步：配置本地认证

**选项 A：使用 .pypirc 文件（推荐）**

在 `C:\Users\CXi\.pypirc` 文件中写入：

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-你的token值
```

保存后，执行：

```bash
cd c:\Users\CXi\Desktop\stcgal-master
twine upload dist/*
```

**选项 B：直接用命令行指定 token**

```bash
cd c:\Users\CXi\Desktop\stcgal-master
twine upload dist/* --username __token__ --password pypi-你的token值
```

### 第三步：验证上传成功

## 验证上传成功

### 1. 检查 PyPI 官方页面
访问：https://pypi.org/project/stcflash/

### 2. 验证可以从 PyPI 安装
```bash
pip install stcflash
```

### 3. 查看包信息
```bash
pip show stcflash
```

## 常见问题

### 问题 1：密码/Token 错误
- 确保 token 复制正确，没有多余空格
- Token 格式应为 `pypi-XXXXXXX...`

### 问题 2：已存在相同版本
- PyPI 不允许重复上传相同版本的包
- 需要更新 `stcflash/__init__.py` 中的 `__version__` 为新版本号
- 重新构建：`python setup.py sdist bdist_wheel`
- 然后重新上传

### 问题 3：包名已被占用
- 如果 "stcflash" 已被占用，需要使用不同的包名
- 修改 `setup.py` 中的 `name` 参数

### 问题 4：元数据验证失败
```bash
twine check dist/*
```
检查输出中的错误，通常涉及 README 格式或描述信息

## 更新包到新版本

1. 修改 `stcflash/__init__.py`：
```python
__version__ = "0.11"  # 更新版本号
```

2. 提交到 git：
```bash
git add stcflash/__init__.py
git commit -m "Bump version to 0.11"
git push
```

3. 重新构建：
```bash
python setup.py sdist bdist_wheel
```

4. 上传新版本：
```bash
twine upload dist/stcflash-0.11.tar.gz dist/stcflash-0.11-py3-none-any.whl
```

## 完整工作流参考

```bash
# 1. 确保代码已提交到 git
git status
git add .
git commit -m "Latest changes"
git push

# 2. 清理旧的构建文件
rm -r build dist stcflash.egg-info

# 3. 构建包
python setup.py sdist bdist_wheel

# 4. 检查包
twine check dist/*

# 5. 上传到 PyPI
twine upload dist/*
```

## 相关资源

- PyPI 官方文档：https://pypi.org
- Twine 文档：https://twine.readthedocs.io/
- Python 打包指南：https://packaging.python.org/
