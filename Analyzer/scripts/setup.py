import os, re, sys, glob, socket, subprocess

# 74X
#LATEST_NTUPLE_EOS="Skim_Feb22_1AK8JetPt300"
#LATEST_NTUPLE_GRID18="Skim_Feb22_1AK8JetPt300"

# 76X
#LATEST_NTUPLE_EOS="Skim_Apr28_1AK8JetPt300"
LATEST_NTUPLE_EOS="Skim_May21_1AK8JetPt300"
#LATEST_NTUPLE_GRID18="Apr13_edm_Apr01"
#LATEST_NTUPLE_GRID18="Skim_Apr28_1AK8JetPt300"
#LATEST_NTUPLE_GRID18="Jun08"
LATEST_NTUPLE_GRID18="Skim_May21_1AK8JetPt300"

ANA_BASE = os.environ['CMSSW_BASE']+'/src/BoostedRazorAnalysis/Analyzer'
DIR = ANA_BASE+'/ntuple/Latest'


if 'lxplus' in socket.gethostname():
    print 'Running on lxplus'
    print 'Mounting EOS ... ',
    if not os.path.exists(ANA_BASE+'/eos_mount_dir'):
        os.makedirs(ANA_BASE+'/eos_mount_dir')
        os.chmod(ANA_BASE+'/eos_mount_dir', 0444)
    if os.listdir(ANA_BASE+'/eos_mount_dir') == []:
        subprocess.call(['/afs/cern.ch/project/eos/installation/cms/bin/eos.select', '-b', 'fuse', 'mount', 'eos_mount_dir'])
    print 'Done.'
    if os.path.lexists(ANA_BASE+'/ntuple/Latest'):
        print 'Remaking symlinks to latest ntuple location: '+os.path.realpath(ANA_BASE+'/ntuple/eos/'+LATEST_NTUPLE_EOS)+' ... ',
        os.remove(ANA_BASE+'/ntuple/Latest')
    else:
        print 'Making symlinks to latest ntuple location: '+os.path.realpath(ANA_BASE+'/ntuple/eos/'+LATEST_NTUPLE_EOS)+' ... ',
    os.symlink('eos/'+LATEST_NTUPLE_EOS, os.path.realpath(ANA_BASE+'/ntuple/Latest'))
    print 'Done.'
elif 'grid18.kfki.hu' in socket.gethostname():
    print 'Running on grid18 (Budapest)'
    if os.path.lexists(ANA_BASE+'/ntuple/Latest'):
        print 'Remaking symlinks to latest ntuple location: '+os.path.realpath(ANA_BASE+'/ntuple/grid18/'+LATEST_NTUPLE_GRID18)+' ... ',
        os.remove(ANA_BASE+'/ntuple/Latest')
    else:
        print 'Making symlinks to latest ntuple location: '+os.path.realpath(ANA_BASE+'/ntuple/grid18/'+LATEST_NTUPLE_GRID18)+' ... ',
    os.symlink('grid18/'+LATEST_NTUPLE_GRID18, os.path.realpath(ANA_BASE+'/ntuple/Latest'))
    print 'Done.'
else:
    print "Error: not on lxplus or grid18 (Budapest)"
    sys.exit()

print "Creating file lists ... ",
if not os.path.exists(ANA_BASE+'/filelists/data'): os.mkdirs(ANA_BASE+'/filelists/data')
if not os.path.exists(ANA_BASE+'/filelists/signals'): os.mkdirs(ANA_BASE+'/filelists/signals')
if not os.path.exists(ANA_BASE+'/filelists/backgrounds'): os.mkdirs(ANA_BASE+'/filelists/backgrounds')
for txtfile in glob.glob('filelists/*/*.txt'):
    os.remove(txtfile)

for directory in os.listdir(DIR):
    if os.path.isdir(DIR+'/'+directory):
        if os.listdir(DIR+'/'+directory):
            # Data
            if re.compile('.*20[1-2][0-9][A-J].*').match(directory):
                flist = open(ANA_BASE+'/filelists/data/'+directory+'.txt', 'w')
                for files in os.listdir(DIR+'/'+directory):
                    filename = os.path.realpath(DIR+'/'+directory+'/'+files)
                    print>>flist, filename
            # Signals
            elif re.compile('.*T[1-9][t,b,c,q][t,b,c,q].*').match(directory):
                flist = open(ANA_BASE+'/filelists/signals/'+directory+'.txt', 'w')
                for files in os.listdir(DIR+'/'+directory):
                    filename = os.path.realpath(DIR+'/'+directory+'/'+files)
                    print>>flist, filename
            # Backgrounds
            else:
                flist = open(ANA_BASE+'/filelists/backgrounds/'+directory+'.txt', 'w')
                for files in os.listdir(DIR+'/'+directory):
                    filename = os.path.realpath(DIR+'/'+directory+'/'+files)
                    print>>flist, filename

print 'Done.'