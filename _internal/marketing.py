import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    # Try to keep the text simple, one or two words.
    text = """ComputeText"""
    font_name = "IBMPlexMono-Bold"  # For code
    # font_name = "IBMPlexSans-Medium"  # For text
    font_size = 250  # You may need to decrease this
    return font_name, font_size, text


@app.cell
def __(font_name, font_size, mo, text):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import os
    import base64
    from textwrap import dedent

    width = 1944
    height = 1024
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(f"fonts/{font_name}.ttf", font_size)
    except IOError:
        print("Couldn't load font")
        font = ImageFont.load_default(font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2
    draw.text((x, y), text, font=font, fill="black")
    buffered = BytesIO()
    image.save(buffered, format="PNG")

    img_str = base64.b64encode(buffered.getvalue())
    base_img_data = f"data:image/png;base64,{img_str.decode('ascii')}"
    mo.image(base_img_data)
    return (
        BytesIO,
        Image,
        ImageDraw,
        ImageFont,
        base64,
        base_img_data,
        bbox,
        buffered,
        dedent,
        draw,
        font,
        height,
        image,
        img_str,
        os,
        text_height,
        text_width,
        width,
        x,
        y,
    )


@app.cell
def __(mo):
    # Create a form with multiple elements
    form = (
        mo.md("""
        ## Click submit to generate

        #### Alternate prompts
        - satellite view of a landscape lit by city lights
        - high altitude drone footage birds eye view clouds and crashing turbulent ocean waves at sunrise
        - high altitude drone footage birds eye view of mountain range with clouds and crashing turbulent ocean waves at sunset

        {gen_prompt}
        
        #### Alternate prompts
        - highly detailed anime scene miyazaki ghost in the shell bright colors
        - highly detailed art deco illustration
        - highly detailed woodblock print hokusai bold lines bright colors

        {upscale_prompt}
    """)
        .batch(
            gen_prompt=mo.ui.text_area(
                label="generate prompt",
                value="high altitude drone footage birds eye view clouds and crashing turbulent ocean waves at sunrise",
            ),
            upscale_prompt=mo.ui.text_area(
                label="upscale prompt",
                value="highly detailed woodblock print hokusai bold lines bright colors",
            ),
        )
        .form(show_clear_button=True, bordered=False)
    )
    form
    return form,


@app.cell
def __(os):
    from substrate import (
        Substrate,
        GenerateImage,
        StableDiffusionXLControlNet,
        RemoveBackground,
        UpscaleImage,
    )

    api_key = os.environ.get("SUBSTRATE_API_KEY")
    substrate = Substrate(api_key=api_key)
    return (
        GenerateImage,
        RemoveBackground,
        StableDiffusionXLControlNet,
        Substrate,
        UpscaleImage,
        api_key,
        substrate,
    )


@app.cell
def __(
    RemoveBackground,
    StableDiffusionXLControlNet,
    UpscaleImage,
    base_img_data,
    form,
    substrate,
):
    mask = RemoveBackground(
        image_uri=base_img_data,
        return_mask=True,
    )
    prompt = form.value["gen_prompt"]
    controlnet = StableDiffusionXLControlNet(
        image_uri=mask.future.image_uri,
        prompt=prompt,
        control_method="illusion",
        conditioning_scale=0.9,
        strength=0.6,
        num_images=1,
    )
    upscale = UpscaleImage(
        image_uri=controlnet.future.outputs[0].image_uri,
        prompt=f"{form.value["upscale_prompt"]} {prompt}",
        output_resolution=2048,
    )
    res = substrate.run(upscale)
    return controlnet, mask, prompt, res, upscale


@app.cell
def __(controlnet, mask, mo, res, upscale):
    mo.vstack(
        [
            mo.hstack(
                [
                    mo.image(res.get(mask).image_uri),
                    mo.image(res.get(controlnet).outputs[0].image_uri),
                ]
            ),
            mo.image(res.get(upscale).image_uri),
        ]
    )
    return


@app.cell
def __(BytesIO, Image, ImageDraw, base64, font, height, text, width, x, y):
    import re
    import numpy as np
    from PIL import ImageChops


    def dilate(image, iterations=1):
        image_array = np.array(image)
        kernel = np.ones((3, 3), np.uint8)
        for _ in range(iterations):
            image_array = np.pad(image_array, 1, mode="constant")
            dilated = np.zeros_like(image_array)
            for i in range(1, image_array.shape[0] - 1):
                for j in range(1, image_array.shape[1] - 1):
                    dilated[i, j] = np.max(image_array[i - 1 : i + 2, j - 1 : j + 2] * kernel)
            image_array = dilated[1:-1, 1:-1]
        return Image.fromarray(image_array)


    def draw_text(img, x, y, text, font, outline_color, outline_width=2):
        text_img = Image.new("L", img.size, 0)
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((x, y), text, font=font, fill=255)
        outline_img = dilate(text_img, iterations=outline_width)
        hollow_outline = ImageChops.subtract(outline_img, text_img)
        outline_rgba = Image.new("RGBA", img.size, (0, 0, 0, 0))
        outline_rgba.putalpha(hollow_outline)
        colored_outline = Image.new("RGBA", img.size, outline_color)
        colored_outline.putalpha(hollow_outline)
        result = Image.alpha_composite(img, colored_outline)
        return result


    def final_image(image_uri):
        base64_string = re.sub(r"^data:image/.+;base64,", "", image_uri)
        image_data = base64.b64decode(base64_string)
        original_image = Image.open(BytesIO(image_data)).convert("RGBA")
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        finalimg = Image.new("RGBA", resized_image.size, (255, 255, 255, 0))
        finalimg.paste(resized_image, (0, 0), resized_image)

        outline_color = (255, 255, 255, 255)
        outline_width = 3

        finalimg = draw_text(finalimg, x, y, text, font, outline_color, outline_width)

        finalbuff = BytesIO()
        finalimg.save(finalbuff, format="PNG")
        finalimg_str = base64.b64encode(finalbuff.getvalue()).decode("ascii")
        return f"data:image/png;base64,{finalimg_str}"
    return ImageChops, dilate, draw_text, final_image, np, re


@app.cell
def __(final_image, mo, res, upscale):
    upscale_final = final_image(res.get(upscale).image_uri)
    mo.image(upscale_final)
    return upscale_final,


@app.cell
def __(mo, text, upscale_final):
    mo.download(upscale_final, filename=f"{text}.png")
    return


if __name__ == "__main__":
    app.run()
