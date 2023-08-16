from setuptools import setup

setup(
    name='geokakao',
    version='0.0.1',
    description='Geospatial Features Using Kakao API',
    author='Byeong-Hyeok Yu',
    author_email='bhyu@knps.or.kr',
    url='https://github.com/osgeokr/geokakao',
    packages=['geokakao'],
    install_requires=[
        'requests',
        'pandas',
        'geopandas',
        ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6',
    ],
)
