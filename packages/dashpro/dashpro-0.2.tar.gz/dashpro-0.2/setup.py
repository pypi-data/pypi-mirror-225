from setuptools import setup, find_packages

setup(
    name='dashpro',           # Replace with your app's name
    version='0.2',                 # Replace with your app's version
    description='A dynamic Django dashboard ',
    long_description='dashpro is a Django admin dashboard with better UI/UX expirence and provides you with more control for your website such as custom widgets custom actions and analysis for you models creation and users sessions , comming soon : API intgeration ',
    author='Hussein Naim',
    author_email='ehusseinnaim@gmail.com',
    url='https://github.com/ehusseinnaim/Dashpro.git',  # Replace with your app's GitHub repository URL
    packages=find_packages(),
    install_requires=[
        'Django>=4.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
