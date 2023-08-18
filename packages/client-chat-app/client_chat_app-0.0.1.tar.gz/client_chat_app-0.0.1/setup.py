from setuptools import setup, find_packages


setup(name="client_chat_app",
      version="0.0.1",
      description="client",
      author="dmitrycider",
      author_email="dimkasidorow@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
