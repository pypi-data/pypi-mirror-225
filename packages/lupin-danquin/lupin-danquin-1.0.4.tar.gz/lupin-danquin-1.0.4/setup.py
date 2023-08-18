from setuptools import setup


from lupin_danquin.core.tools.utils import update_version


if __name__ == '__main__':
    setup(
        version=update_version()
    )
