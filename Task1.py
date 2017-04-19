import parsing as par
import os,csv
import numpy as np
from PIL import Image
root_path=os.path.dirname(__file__)
class scan:
    """
     holds the label path and dicom path together
    """
    def __init__(self, label, dicom):
        self.label = label
        self.dicom = dicom
        self.generate_mask()
    def generate_mask(self):
        """
         Generated mask based on label path. Also performs checks of correctness of mask
        """
        try:
            if os.path.isfile(self.label):
                coords=par.parse_contour_file(self.label)
                mask=par.poly_to_mask(coords,256,256)
                self.label = self.label.split('.')[0] + 'GT.png'
                Image.fromarray(np.uint8(mask) * 255).save(self.label, 'PNG')
                #Image.fromarray(np.multiply(np.uint8(mask),par.parse_dicom_file(self.dicom)['pixel_data'])).save('test/1.png', 'PNG')
            else:
                pass
                self.label=self.label.split('.')[0] + 'GT.png'
                Image.fromarray(np.zeros((256,256),dtype='uint8')).save(self.label, 'PNG')
        except :
            print('Mask Generation failed')

class patient:
    def __init__(self,dicom_folder,label_folder):
        self.label_folder=os.path.join(root_path,'contourfiles',label_folder,'i-contours')
        self.dicom_folder=os.path.join(root_path,'dicoms',dicom_folder)
        self.scans,self.scans_info = self.loadscans(self.label_folder,self.dicom_folder)

    def loadscans(self,label_folder,dicom_folder):
        scans = []
        scans_info=[]
        # create a list of scans with labels for each patient
        # Generate label file name for now
        try:
            for dicom_file in os.listdir(dicom_folder):
                label_file='IM-0001-' +str(int(dicom_file.split('.')[0])).zfill(4) + '-icontour-manual.txt'
                current_scan=scan(os.path.join(label_folder, label_file), os.path.join(dicom_folder, dicom_file))
                scans.append(current_scan)
                scans_info.append([current_scan.dicom,current_scan.label])
        except:
            print('Path does not exist '+dicom_folder)
        return scans,scans_info

    def getscans(self):
        return self.scans_info

        pass
if __name__ == "__main__":
    # Driver code
    # Read link.csv
    with open('link.csv', 'rb') as f:
        reader = csv.reader(f)
        patient_list = list(reader)
    patients=[]
    all_scans=[]
    for i in range(1,len(patient_list)):
        patients.append(patient(patient_list[i][0],patient_list[i][1]))

    # get all scans into one list and save as csv
    for patient in patients:
        all_scans= all_scans+patient.getscans()
    file = open('train.csv', 'wb')
    wr = csv.writer(file)
    wr.writerows(all_scans)


