import os
import subprocess
import glob

from ._scf import _LogStart
_lg=_LogStart().setup()


"""
subcommand common functions (scf) used by ./subcommands
"""

def call_ffmpeg(pngfolder,fps_pass=None,outputdir=None):
    """function that actually calls ffmpeg to stitch all the png together
    
    :pngfolder: folder where all the pngs are that we are stitching together
    :fps_pass (optional): 
    :returns: None (except for a movie!)
    """
    #ollie's command didn't work on storm
    # os.chdir(pngfolder)
    # subprocess.call('ffmpeg -framerate 10 -y -i moviepar%05d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4')

    # ffmpeg ideas:
    # ffmpeg -r 15 -i moviepar%05d.png -b 5000k -vcodec libx264 -y -an movie.mov

    _lg.info("Stitching frames together (might take a bit if you have lots of frames)...")

    FNULL = open(os.devnull, 'w')

    if fps_pass is not None:
        fps=str(fps_pass)
    else:
        fps=str(15)

    quality='20'
    if outputdir:
        os.chdir(pngfolder)
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an '+outputdir,shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
    else:
        os.chdir(pngfolder)
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

    #remove png
    if os.path.isfile(pngfolder+'movie.mov') or os.path.isfile(outputdir):
        ifiles=sorted(glob.glob(pngfolder+ 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find any symlinks to remove anything!"
        for f in ifiles:
            os.remove(f)

        if os.path.isfile(pngfolder+'movie.mov'):
            _lg.info("MkMov SUCCESS, check it out: "+pngfolder+'movie.mov')

        if outputdir:
            if os.path.isfile(outputdir):
                _lg.info("MkMov SUCCESS, check it out: "+outputdir)
    else:
        _lg.info("MkMov FAIL")
        _lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
        sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
