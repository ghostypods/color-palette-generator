from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

# -------------------------------- DON'T FORGET ABOUT THE SECRET KEY!!! --------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)


def extract_dominant_colors(image_path, num_colors):
    img = Image.open(image_path)
    img = img.resize((200, 200))  # Resize for faster processing
    img_array = np.array(img)
    pixels = img_array.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, random_state=0)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    return colors


# Function to convert RGB to Hex
def rgb_to_hex(colors):
    hex_codes = ['#%02x%02x%02x' % tuple(color) for color in colors]
    return hex_codes


# Flask function to display palette
def display_color_palette(colors):
    plt.figure(figsize=(8, 2))
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    for i, color in enumerate(colors):
        plt.subplot(1, len(colors), i + 1)
        plt.imshow([[color / 255]])
        plt.axis('off')
    plt.show()


@app.route("/", methods=['GET', 'POST'])
def home():
    hex_codes = []
    if request.method == 'POST':
        image = request.files.get('file_path')

        if image:
            try:
                palette = extract_dominant_colors(image, 10)
                hex_codes = rgb_to_hex(palette)
            except ValueError:
                flash("There was an error with the file you uploaded, \n please try again or select another file")
                redirect(url_for('home'))
        else:
            print("error with the image uploaded, please try again or upload a different image")

    return render_template('home.html', hex_codes=hex_codes)


if __name__ == "__main__":
    app.run(debug=True)
