from setuptools import setup, find_packages

setup(
    name='ThalamusEngine',
    version='0.1.7',
    description='ThalamusEngine for Recognition of 3D',
    author='Thomas A. Anderson',
    author_email='pjtthalamus@gmail.com',
    url='https://github.com/Thomas-Anderson1999',
    license='MIT',
    py_modules=['ThalamusEngine'],
    packages=['ThalamusEngine'],
    install_requires=[
        'opencv-python>=4.0',
        'opencv-contrib-python>=4.0'
    ],
    #package_data={'Lib': ['Lib/freeglut.dll', 'Lib/opencv_world450d.dll.dll', 'Lib/thalamus.dll', 'Lib/thalamus.so']},
    package_data={'ThalamusEngine': ['Lib/*']},
    keywords=['OpenGL', 'Renderer', 'Thalamus'],
    python_requires='>=3.6',
    zip_safe=False
)
