'''
@date 1/1/25

@brief      A collection of tools for manipulating files
'''
import xml.etree.ElementTree as Xet
import glob, os

def get_all_files_with_ext(dir, ext):
    '''returns a list of files with specific extention'''
    os.chdir(dir)
    files = []
    for file in glob.glob(f"*.{ext}"):
        file_with_path = os.path.join(dir,file)
        print(file_with_path)
        files.append(file_with_path)
    return files

def convert_xml_to_csv(xml_file):
    '''parse xml file from top to bottom from parent tag to deeper tags'''
    xmlparse = Xet.parse(xml_file)
    root = xmlparse.getroot()
    with open(xml_file+".txt", 'a') as output_file:
        for i in root: # xml level1
            # print(i.tag, i.text, end = '')
            for i in i: # xml level2
                if len(i) >0:
                    print(i.tag,'=',i.items())
                    output_file.write(i.tag+"="+str(i.tems())+'\n')
                else:
                    print(i.tag,'=',i.text)
                    output_file.write(i.tag+'='+i.text+'\n')
                for index, i in enumerate(i): # xml level3
                    for i in i:
                        print(' | ',i.tag, i.text, end = ' ')

if __name__ == '__main__':
    #xmlfiles = get_all_files_with_ext(this_script_location,'xml')
    pass