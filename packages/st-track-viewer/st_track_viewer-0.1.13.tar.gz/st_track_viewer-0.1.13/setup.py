import setuptools

setuptools.setup(
    name="st_track_viewer",
    version="0.1.13",
    author="Elliot Glas",
    author_email="elliot.glas@viscando.com",
    description="A Streamlit component for visualizing track data on images",
    long_description="""
      st-track-analysis
      ================

      st-track-analysis is a Python package that provides a custom Streamlit component for visualizing track data on images. It allows you to easily plot and analyze tracks with associated ground data on top of images.

      Features
      --------
      - Supports visualizing multiple tracks with their associated ground data on the same image.
      - Easily overlay shape data, such as bounding boxes, on the images.
      - Option to provide names for each track for better identification.
      - Customizable key for using the component in Streamlit apps.
      - Automatic conversion of images created by matplotlib into base64-encoded URLs for display.

      Requirements
      ------------
      - Python 3.x
      - streamlit
      - matplotlib
      """,
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
