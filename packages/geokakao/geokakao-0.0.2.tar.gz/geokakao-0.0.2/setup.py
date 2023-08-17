from setuptools import setup

setup(
    name='geokakao',
    version='0.0.2',
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
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
