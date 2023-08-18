from setuptools import setup, find_packages


setup(name="server_chat_app",
      version="0.0.1",
      description="server",
      author="dmitrycider",
      author_email="dimkasidorow@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
