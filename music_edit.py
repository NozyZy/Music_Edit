import os
import re
import music_tag
from PIL import Image, ImageDraw, ImageFont

song_formats = {
    'aac': 'aac',
    'aiff': 'aiff',
    'dsf': 'dsf',
    'flac': 'flac',
    'm4a': 'm4a',
    'mp3': 'mp3',
    'ogg': 'ogg',
    'opus': 'opus',
    'wav': 'wav',
    'wv': 'wv'
}

artwork_formats = {
    'jpg': 'jpg',
    'jpeg': 'jpeg',
    'png': 'png'
}

font_path = os.path.abspath('Roboto-Regular.ttf')

end = False
is_good = False

banner = """\033[97m
ooo        ooooo                       o8o                 oooooooooooo       .o8   o8o      .   
`88.       .888'                       `"'                 `888'     `8      "888   `"'    .o8   
 888b     d'888  oooo  oooo   .oooo.o oooo   .ooooo.        888          .oooo888  oooo  .o888oo 
 8 Y88. .P  888  `888  `888  d88(  "8 `888  d88' `"Y8       888oooo8    d88' `888  `888    888   
 8  `888'   888   888   888  `"Y88b.   888  888             888    "    888   888   888    888   
 8    Y     888   888   888  o.  )88b  888  888   .o8       888       o 888   888   888    888 . 
o8o        o888o  `V88V"V8P' 8""888P' o888o `Y8bod8P'      o888ooooood8 `Y8bod88P" o888o   "888"\033[0m
                                                                            v1.0.4 by \033[94mNozZy\033[0m
"""


while not end:
    os.system("cls")
    print(banner)

    song_format = ''
    song_files = []
    artwork_files = []
    album = ''
    artist = ''
    release_year = ''
    artwork_song = ''
    replace_mode = False

    while not is_good:
        dir_path = ''
        while not dir_path and not os.path.isdir(dir_path):
            dir_path = input("Specify the album directory : ")

        guess = dir_path.split('/')[-1].split('\\')[-1]
        album = input(f"Specify the album name ({guess}) : ").strip()

        if replace_mode or not album.strip():
            album = guess

        guess = dir_path.split("/" + album)[0].split("\\" + album)[0].split('/')[-1].split('\\')[-1]
        artist = input(f"Specify artist's name ({guess}) : ").strip()

        if replace_mode or not artist.strip():
            artist = guess

        pattern = input('File name patern to be removed ? (eg. "Game Soundtrack") : ').strip()
        if pattern:
            pattern = re.compile(pattern, flags=re.IGNORECASE)

        release_year = input(f"Specify the release year (unknown) : ").strip()

        #  Get files and sort them by creation date
        os.chdir(dir_path)
        files = filter(os.path.isfile, os.listdir(dir_path))
        files = [os.path.join(dir_path, f) for f in files]
        files.sort(key=lambda x: os.path.getctime(x))

        # Get only valid song and artwork files
        for file in files:
            file_format = file.split('.')[-1]
            if file_format in song_formats.values():
                song_files.append(file)
                song_format = file_format
            elif file_format in artwork_formats.values():
                artwork_files.append(file)

        # CHoosing right artwork image
        j = 0
        artwork_song = ''
        if len(artwork_files) > 1:
            print("Opening artwork images. Please wait...\n")
            for artwork in artwork_files:
                with Image.open(artwork).convert("RGBA") as base:
                    j += 1
                    artwork_name = artwork.split('/')[-1].split('\\')[-1]
                    outname = f"{str(j)} - {artwork_name}"
                    print(outname)
                    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
                    font = ImageFont.truetype(font_path, 64)
                    draw = ImageDraw.Draw(txt)
                    draw.text((10, 10), outname, font=font, fill=(255, 0, 0, 255))
                    out = Image.alpha_composite(base, txt)
                    out.show()

            artwork_choice = int(input("Specify the artwork image number (0 for none) : "))
            if artwork_choice:
                artwork_song = artwork_files[artwork_choice - 1]

        elif len(artwork_files) == 1:
            artwork_song = artwork_files[0]
            print("Found artwork image :", artwork_song)
     
        else:
            print("No artwork image found. Put it in the directory next time (.png, .jpg, .jpeg)")

        print(f"\n"
              f"Album : {album}\n"
              f"Artist : {artist}\n"
              f"Year : {release_year}\n"
              f"Artwork : {artwork_song}\n"
              f"Songs directory : {dir_path}\n")

        yesno = input("Is this correct ? Y/n : ")
        if yesno.lower().strip() == 'y':
            is_good = True
        else:
            is_good = False

        yesno = input("\nReplace mode (force) ? Y/n : ")
        if yesno.lower().strip() == 'y':
            replace_mode = True
        else:
            replace_mode = False

    print("\nApplying...\n")
    song_names = []
    i = 0
    for file in song_files:
        text = ''
        i += 1
        name = file.split('\\')[-1].split('.')
        name.pop()
        name = '.'.join(name).strip()
        if pattern:
            name = re.sub(pattern, '', name)
        reg_paranth = r"((?:\(|\[)[!-z\u00C0-\u017F\s.]+(?:\)|\])[-\s]+)|([-\s]+(?:\(|\[)[!-z\u00C0-\u017F\s.]+(?:\)|\]))"
        name = re.sub(reg_paranth, '', name).strip('-/\\")')
        name = name.split('-')
        for n in name:
            if artist.lower() in n.lower().strip() :
                name.pop(name.index(n))
        name = '-'.join(name).strip('- \\/')
        

        f = music_tag.load_file(file)
        if replace_mode or not f['tracktitle']:
            f['tracktitle'] = name
            text += name + ' : '
        if replace_mode or not f['tracknumber']:
            f['tracknumber'] = i
            text += f"N°{str(i)} - "
        if replace_mode or not f['artist']:
            f['artist'] = artist
            text += f"{artist} - "
        if replace_mode or not f['albumartist']:
            f['albumartist'] = artist
        if replace_mode or not f['album']:
            f['album'] = album
            text += f"{album} - "
        if replace_mode or not f['totaltracks']:
            f['totaltracks'] = len(song_files)
        if release_year and (replace_mode or not f['year']):
            f['year'] = release_year
            text += f"{release_year}"
        if artwork_song and (replace_mode or not f['artwork']):
            with open(artwork_song, 'rb') as img_in:
                f['artwork'] = img_in.read()
                text += f" - {artwork_song}"

        if text:
            print(text)
        f.save()
        try:
            os.rename(file, name + "." + song_format)
        except Exception:
            pass

    print("Applied !")

    yesno = input("\nDo you want to edit another album ? Y/n : ")
    if yesno.lower().strip() == 'y':
        end = False
        is_good = False
    else:
        end = True
