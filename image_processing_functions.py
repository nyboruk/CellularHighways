# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:11:00 2017

@author: Robyn.Pritchard
"""
from tkinter import filedialog 
import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils as imu
from threading import Thread
from queue import Queue

class FileVideoStream:
    def __init__(self, path, queueSize = 128):
        self.cap = cv2.VideoCapture(path)
        self.ret = False
        
        self.Q = Queue(maxsize = queueSize)
    
    def start(self):
        t = Thread(target = self.update, args = ())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            
            if not self.Q.full():
                (ret, frame) = self.cap.read()
                if not ret:
                    self.stop()
                    return
                self.Q.put(frame)
    
    def read(self):
        return self.Q.get()
    
    def more(self):
        return self.Q.qsize()>0
    
    def stop(self):
        self.stopped - True

class bead_data(object):
    
    def __init__(self, length = 1e6):
        self.length = np.int64(length)
        self.data = np.zeros((self.length,10))
        self.dat = 0
        self.sortwindow = 0
        
    def reset(self):
        self.data = np.zeros((self.length,10))
        
    def save(self):
        my_header = '# bead_num, area , sorted? , stationary?, other?, xposition, yposition , slice, sort x, sort y'
        save_name = filedialog.asksaveasfilename()
        self.find_valid()
        np.savetxt(save_name + ".csv", self.dat, delimiter = "," , header = my_header)
    
    def load(self):
        filepath = filedialog.askopenfilename()
        self.data = np.genfromtxt(filepath, dtype = float, delimiter = ',', skip_header = 1)
        self.find_valid()
        
    def find_valid(self):
        valid = self.data[:,0]
        self.dat = self.data[(valid>0)]
        
    def plot_all_beads(self):
        plt.figure()
        plt.scatter(self.dat[:,5],self.dat[:,6])
        plt.xlabel('x pixels')
        plt.ylabel('y pixels')
        plt.title('all bead positions')
        plt.gca().invert_yaxis()
    
    def plot_separated_beads(self):
        bead_data = self.dat[np.argsort(self.dat[:,5])]
        paired = bead_data[:,8]
        station = bead_data[:,3]
        pairs = bead_data[(paired > 0), :]
        npairs = bead_data[(paired == -1), :]
        npairs2 = bead_data[((paired == 0) & (station == 1)),:]
        obeads =  bead_data[(bead_data[:,4] == 1), :]
        cxmax = np.max(pairs[:,5])
        cxmin = np.min(pairs[:,5])
        cols = ((pairs[:,5]-cxmin)/(cxmax-cxmin))*100
        cm = plt.cm.get_cmap('RdYlBu')
        
        plt.figure()

        plt.scatter(obeads[:,5],obeads[:,6], c = 'r')
        plt.scatter(npairs2[:,5], npairs2[:,6], c = 'r')
        plt.scatter(npairs[:,5], npairs[:,6], c = 'black')
        plt.scatter(pairs[:,5], pairs[:,6], c = cols, cmap = cm)
        plt.scatter(pairs[:,8], pairs[:,9], c = cols, cmap = cm)

        plt.gca().invert_yaxis()
        plt.xlabel('x pixels')
        plt.ylabel('y pixels')
        plt.title('organised bead positions')
    
    def plot_separated_beads_image(self, original):
        
        bead_data = self.dat[np.argsort(self.dat[:,5])]
        paired = bead_data[:,8]
        station = bead_data[:,3]
        pairs = bead_data[(paired > 0), :]
        npairs = bead_data[(paired == -1), :]
        npairs2 = bead_data[((paired == 0) & (station == 1)),:]
        obeads =  bead_data[(bead_data[:,4] == 1), :]
        cxmax = np.max(pairs[:,5])
        cxmin = np.min(pairs[:,5])
        cols = ((pairs[:,5]-cxmin)/(cxmax-cxmin))*100
        cm = plt.cm.get_cmap('RdYlBu')
        
        plt.figure()
        plt.imshow(original, cmap='gray', origin = 'lower')

        plt.scatter(obeads[:,5],obeads[:,6], c = 'r')
        plt.scatter(npairs2[:,5], npairs2[:,6], c = 'r')
        plt.scatter(npairs[:,5], npairs[:,6], c = 'black')
        plt.scatter(pairs[:,5], pairs[:,6], c = cols, cmap = cm)
        plt.scatter(pairs[:,8], pairs[:,9], c = cols, cmap = cm)

        plt.gca().invert_yaxis()
        plt.xlim([0,np.size(original,1)])
        plt.xlabel('x pixels')
        plt.ylabel('y pixels')
        plt.title('organised bead positions')
    
    def plot_sort_window(self, set_x_lim = False, x_low_lim = 0, x_up_lim = 0):
        plt.figure()
        
        plt.subplot(211)
        plt.errorbar(self.sort_window[:,0], self.sort_window[:,1], yerr = [self.sort_window[:,3],self.sort_window[:,2]], mfc='red', fmt='--', barsabove=False, capsize = 3)
        
        if set_x_lim: plt.xlim([x_low_lim, x_up_lim])
        
        plt.ylim([-5,110])
        plt.xlabel('pixels')
        plt.ylabel('% sorted')
        plt.subplot(212)

        plt.bar(self.sort_window[:,0],self.sort_window[:,4], color = 'r')
        if set_x_lim: plt.xlim([x_low_lim, x_up_lim])
        
        plt.xlabel('pixels')
        plt.ylabel('number of beads')
        plt.tight_layout()
    
    def find_sort_window(self, bins = 40, conv = 1, off_set = 0, setlims = False, xlower = 0, xupper = 0):
        self.find_valid()
        station_val = self.dat[:, 3]
        paired = self.dat[:,8]
        stations = self.dat[((station_val == 1) & (paired!=0)), :]
        x_vals = stations[:, 5]
        
        min_x = np.min(x_vals)
        max_x = np.max(x_vals)
        if setlims:
            min_x = xlower
            max_x = xupper
            
        diff = (max_x - min_x)/bins
        
        self.sort_window = np.zeros((bins,5))
        
        for hh in np.arange(0,bins):
            
            bin_lower = min_x+hh*diff
            bin_upper = min_x+(hh+1)*diff
            vals = stations[((x_vals > bin_lower ) & (x_vals < bin_upper)),8]
            sorts = vals[vals>0]
            num_sort_counts = np.size(sorts)
            n = np.size(vals)
    
            if n != 0:
                num_sort_counts = num_sort_counts
                p = (num_sort_counts/n)
                pc = p*100
                #Wilson score interval
                ec = np.sqrt(p*(1-p)/n)*100
                z = 1
                e_f = (1/(1+(1/n)*z*z))
                e_pm = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))
                e_top = e_f * (p + z*z/(2*n) + e_pm)
                e_bot = e_f * (p + z*z/(2*n) - e_pm)
                ep_top = 100*(e_top-p)
                ep_bot = 100*(p-e_bot)
                #wilson score interval with correction
    #            ews_bot = (2*n*p+z*z-z*np.sqrt(z*z-(1/n)+4*n*p*(1-p)+4*p-2)-1)/(2*(n+z*z))
    #            if ews_bot < 0: ews_bot = 0
    #            ews_top = (2*n*p+z*z+z*np.sqrt(z*z-(1/n)+4*n*p*(1-p)+4*p-2)+1)/(2*(n+z*z))
    #            if ews_top > 1: ews_top = 1
    #            epws_bot = 100 * (p-ews_bot)
    #            epws_top = 100 * (ews_top-p)
            else:
                pc = 0
                ec = 0
                ep_top = 0
                ep_bot = 0
                epws_top = 0
                epws_bot = 0
            self.sort_window[hh,:] = [((hh+0.5)*diff+min_x)*conv-off_set, pc, ep_top, ep_bot, n]
        
        self.plot_sort_window(setlims, xlower, xupper)
    

def nothing(x):
    pass
  
def crop_image(image, ROI):
    ''' returns cropped image from an ROI type'''

    return image[int(ROI[1]):int(ROI[1]+ROI[3]),int(ROI[0]):int(ROI[0]+ROI[2])]    

def get_crop(frame):
    ''' opens up input frame to let you select a region of interest, returns the region of interest (ROI)'''
    
    ROI = cv2.selectROI("Select window", frame)
    cv2.destroyWindow("Select window")
    return ROI

def detector_setup(settings):
    '''Function to setup the bead detection algorithm
        
    '''
    params = cv2.SimpleBlobDetector_Params()
    params.blobColor = 0;
    
    # Change thresholds
    params.minThreshold = settings.detection['MIN_THRESH'].value
    params.maxThreshold = settings.detection['MAX_THRESH'].value

    # Filter by Area.
    params.filterByArea = True
  
    params.minArea = settings.detection['MIN_AREA'].value
    params.maxArea = settings.detection['MAX_AREA'].value
    
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = settings.detection['BEAD_CIRC'].value
    
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def sort_region(frame):
    sROI = cv2.selectROI("Select sorted region", frame)
    cv2.destroyWindow("Select sorted region")
    return sROI

def mask_region(frame):
    mROI = cv2.selectROI("Select stationary bead area", frame)
    cv2.destroyWindow("Select stationary bead area")
    return mROI

def mask_station_bead(avg, settings, mask_waste, mask_sort):
    ROI = settings.detection['SBROI'].value
    mean_station = np.mean(avg[ROI[1]:(ROI[1]+ROI[3]), ROI[0]:(ROI[0]+ROI[2])])
    avg[ROI[1]:(ROI[1]+ROI[3]),ROI[0]:(ROI[0]+ROI[2])] = mean_station
    if settings.general['MASKS_ON'].value:
        mean_sort = np.mean(avg[mask_sort])
        mean_waste = np.mean(avg[mask_waste])
        avg[mask_sort] = mean_sort
        avg[mask_waste] = mean_waste
    return avg

def draw_info(src, counts, settings):
    
    if counts.iframe == 0: counts.iframe = 1
    if counts.valid_frame == 0: counts.valid_frame = 1
    
    display_text = counts.disp_str()
    cv2.putText(src, display_text, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0)) 
    if settings.general['DRAW_ROIS'].value:
        ROIstation = settings.detection['SBROI'].value
        ROIsort = settings.detection['SROI'].value
        if settings.general['MASKS_ON'].value:
            draw_poly_lines(src, settings)
            cv2.rectangle(src, (ROIstation[0],ROIstation[1]) ,(ROIstation[0]+ROIstation[2],ROIstation[1]+ROIstation[3]), (150,150,150),1)
        else:
            cv2.rectangle(src, (ROIsort[0],ROIsort[1]) ,(ROIsort[0]+ROIsort[2],ROIsort[1]+ROIsort[3]), (150,150,150), 1)
            cv2.rectangle(src, (ROIstation[0],ROIstation[1]) ,(ROIstation[0]+ROIstation[2],ROIstation[1]+ROIstation[3]), (150,150,150),1)
    return src

def extent(cnt):
    ''' function to find the extent of a contours'''
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area = w*h
    ext = float(area)/rect_area
    return ext

def aspect(cnt):
    '''function to find the aspect ratio of a rectange surrounding the contours'''
    x,y,w,h = cv2.boundingRect(cnt)
    aspect_ratio = float(w)/h
    return aspect_ratio

def min_aspect(cnt):
    '''function to find the aspect ratio of the minimum rectange surrounding the contours'''
    rect = cv2.minAreaRect(cnt)
    w = rect[1][0]
    h = rect[1][1]
    if h <= 0:
        min_aspect_ratio = 0
    else:
        min_aspect_ratio = w/h
    return min_aspect_ratio

def solidarity(cnt):
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    if hull_area <= 0:
        solid = 0
    else:
        solid = float(area)/hull_area
    return solid

def offset_angle(p1, p2):
    [x1, y1] = p1
    [x2, y2] = p2
    
    tempx, tempy = 0, 0
    
    if x1 < x2:
        tempx = x1
        tempy = y1
        x1 = x2
        y1 = y2
        x2 = tempx
        y2 = tempy
    ratio = (y2-y1)/(x1-x2)
    theta = 90 + np.arctan(ratio)*(180/np.pi)
    centre = [(x1+x2)/2,(y1+y2)/2]
    separation = np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    return theta, centre, separation

def find_crosses(src):
    imgray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (3,3), 2. )
    th, edges = cv2.threshold(imgray, 30, 255, cv2.THRESH_BINARY_INV)
    im2, contours, hierachy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    contour_data = np.zeros((np.size(contours),5))
    temp_points = np.zeros((np.size(contours),2))
    
    for i, cnt in enumerate(contours):
        [area, ex, sol, asp, min_asp] = [cv2.contourArea(cnt),extent(cnt),solidarity(cnt), aspect(cnt), min_aspect(cnt)]
        contour_data[i,:] = [area, ex, sol, asp, min_asp]

        #extent = 0.36, soildarity = 0.68, AR = 1
        if (area >4000 and area <6000 and sol > 0.5 and sol < 0.7 and min_asp > 0.9 and min_asp < 1.1):
            x,y,w,h = cv2.boundingRect(cnt)
#            cv2.rectangle(src,(x,y),(x+w,y+h),(0,255,0),1)
            rect = cv2.minAreaRect(cnt)
            box  = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(src, [box], -1, (0, 0, 255), 1)
            (x1,y1), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x1), int(y1))
            radius = int(radius)
            cv2.circle(src, center, radius, (255,0,0), 1)
            cv2.circle(src, center, 1, (255,0,0), 2)
            temp_points[i,:] = [x1, y1]
    points = temp_points[(temp_points[:,0]>0),:]
    return points, contour_data

def open_footage(settings):
    ''' opens video footage, either from a saved file or directly from a camera
        depending on the setting'''
        
    if settings.general['LOAD_VIDEO'].value:
        file_path = filedialog.askopenfilename()
        cap = cv2.VideoCapture(file_path)
    else:
        cap = initialise_camera(settings)
        
    return cap

def initialise_camera(settings):
    ''' Tell the program which camera to use and what settings.
    '''
    cap = cv2.VideoCapture(settings.general['CAMERA_NUMBER'].value)
    if settings.general['SETCAMERA'].value:
        cap.set(3, settings.general['CAMX'].value)
        cap.set(4, settings.general['CAMY'].value)
        
    return cap

def initialise(frame1, settings):
    
    settings.general['FRAME_SIZE_RAW'].value = frame1.shape[0:2][::-1]
    
    if settings.general['AUTOALIGN'].value:
        frame1copy = frame1.copy()
        detection_error = False
        points, cdata = find_crosses(frame1)
        
        if np.size(points,0)!=2:
            print("error detecting alignment crosses, manual selection required")
            detection_error = True
            
        if np.size(points,0) == 2:   
            #find crosses pair and rotate image
            angle, centre, separation = offset_angle(points[0], points[1])
            frame1copy = imu.rotate_bound(frame1copy, angle)
            frame1copy = cv2.flip(frame1copy,0)
            
            #find crosses in aligned image
            points2, cdata2 = find_crosses(frame1copy)
            angle2, centre2, ds = offset_angle(points2[0], points2[1])
            
            yoff = np.int64(ds/2)
            xoff = np.int64(3*ds/4)
            [x0, y0] = np.int64(centre2)
            ROI = [x0 - xoff, y0 - yoff, 3*xoff, 2*yoff]
    
            frame1 = crop_image(frame1copy, ROI)
            
            avg = np.float32(cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY))
            cx, cy = xoff, yoff
            
            settings.detection['DS'].value = np.int64(ds)
            settings.detection['CX'].value = np.int64(cx)
            settings.detection['CY'].value = np.int64(cy)
            if settings.general['MASKS_ON'].value:
                [xl0 ,xl1, yl0, yl1, yu0, yu1] = np.int64([cx+0.94438*ds, cx+1.43236*ds, cy+0.028*ds, cy-0.06*ds, cy-0.022*ds, cy-0.11*ds])
                settings.detection['SORTPOINTS'].value = np.array([[xl0, yl0], [xl1, yl1], [xl1, yu1], [xl0,yu0], [xl0,yl0]])
                [xwl0, xwl1, ywl0, ywl1, ywu0, ywu1] = np.int64([cx+1.0592*ds, cx+1.3175*ds, cy+0.2354*ds, cy+0.33584*ds,cy+0.16075*ds,cy+0.26121*ds])
                settings.detection['WASTEPOINTS'].value = np.array([[xwl0,ywl0],[xwl1,ywl1],[xwl1,ywu1],[xwl0,ywu0],[xwl0,ywl0]])
                draw_poly_lines(frame1, settings)
            
            
            sbROI = mask_region(frame1)
            if settings.general['MASKS_ON'].value:
                mask_sort = np.zeros((frame1.shape[0],frame1.shape[1]))
                mask_waste = np.zeros((frame1.shape[0],frame1.shape[1]))
                cv2.fillConvexPoly(mask_sort, settings.detection['SORTPOINTS'].value, 1)
                cv2.fillConvexPoly(mask_waste, settings.detection['WASTEPOINTS'].value, 1)
                mask_sort = mask_sort.astype(np.bool)
                mask_waste = mask_waste.astype(np.bool)

            else:
                mask_waste = 0
                mask_sort = 0
            
            sROI = sort_region(frame1)   
            settings.detection['ANGLE'].value = angle
            settings.detection['ROI'].value = ROI
            settings.detection['SROI'].value = sROI
            settings.detection['SBROI'].value = sbROI

            avg = mask_station_bead(avg, settings, mask_waste, mask_sort)
            

    if settings.general['AUTOALIGN'].value == False or detection_error == True:
        settings.general['MASKS_ON'].value = False
        mask_waste = 0
        mask_sort = 0
        angle = 90
        settings.detection['ANGLE'].value = angle
        if settings.general['ROTATE_FLIP'].value:
            frame1 = imu.rotate_bound(frame1, angle)
            frame1 = cv2.flip(frame1,0)

        if settings.general['CROP'].value:
           ROI = get_crop(frame1)
           frame1 = crop_image(frame1, ROI)       
           settings.detection['ROI'].value = ROI
           
        if settings.general['STATIONARY_ON'].value:
            avg = np.float32(cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY))
            settings.detection['SBROI'].value = mask_region(frame1)
            avg = mask_station_bead(avg, settings, mask_sort, mask_waste)
        settings.detection['SROI'].value = sort_region(frame1)
    
    settings.general['FRAME_SIZE'].value = avg.shape[::-1]

        
    return settings, avg, mask_waste, mask_sort

def draw_poly_lines(src, settings):
    
    cv2.polylines(src,[settings.detection['SORTPOINTS'].value], 1, (0,150,0))
    cv2.polylines(src,[settings.detection['WASTEPOINTS'].value], 1, (0,0,150))
    

def record_start(avg):
    
    video_path = filedialog.asksaveasfilename()
    video_path = video_path + '.avi'
    frameSize = avg.shape[::-1]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    record = cv2.VideoWriter(video_path,fourcc=fourcc, fps=20.0, frameSize=frameSize)
    return record

def rotate_and_flip(src, angle, flip_axis):
    src = imu.rotate_bound(src, angle)
    src = cv2.flip(src, flip_axis)
    return src

def detection_setup(src, avg, detector, settings, mask_waste, mask_sort):
    
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    if settings.general['ROTATE_FLIP'].value: src = rotate_and_flip(src, settings.detection['ANGLE'].value, 0)
    
    if settings.general['CROP'].value:
        src = crop_image(src, settings.detection['ROI'].value)
        original = src.copy()
    else:
        original = src.copy()
    
    if settings.general['DETECTION_ON'].value:
        cv2.accumulateWeighted(src, avg, settings.detection['DECAY'].value)
        if settings.general['STATIONARY_ON'].value:
            avg = mask_station_bead(avg, settings, mask_waste, mask_sort)
        src = cv2.absdiff(src, cv2.convertScaleAbs(avg))
        src = cv2.bitwise_not(cv2.convertScaleAbs(src, alpha = 6))
        src = cv2.GaussianBlur(src, (3,3), 2.)
        
        if settings.general['FILL_HOLES'].value:
            th, src = cv2.threshold(src, settings.detection['MIN_THRESH'].value, 255, cv2.THRESH_BINARY_INV)
            im2, contours, hierachy = cv2.findContours(src, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
            for i, cnt in enumerate(contours):
                contours[i] = cv2.convexHull(cnt)
                area =  cv2.contourArea(contours[i])
                if area < settings.detection['MAX_AREA'].value and area > settings.detection['MIN_AREA'].value:
                    cv2.drawContours(src, [contours[i]], 0, 255, -1)
            src = cv2.bitwise_not(src)
    
    return src, original, avg, detector
    
def find_beads(src, original, detector, settings, counts, beads):
    
    counts.iframe += 1
    frame_sort, frame_stationary, sx, sy, count = 0, 0, 0 ,0, 0
    sbroi = settings.detection['SBROI'].value
    sroi = settings.detection['SROI'].value
    keypoints = detector.detect(src)
    
    if settings.general['SUB_BACKGROUND'].value:
        disp = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
    else:
        disp = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    
    for i in range(0,np.size(keypoints)):
        counts.total_beads += 1                
        x = keypoints[i].pt[0]
        y = keypoints[i].pt[1]
        r = keypoints[i].size/2
        dr = r*1.25
        area = np.pi*np.square(r)
        insort = x > sroi[0] and x < (sroi[0]+sroi[2]) and y < (sroi[1]+sroi[3]) and y > sroi[1]
        
        if insort:
            sort_status = 1
            stationary_status = 0
            out_side_status = 0
            frame_sort += 1
            cv2.circle(disp, (int(x),int(y)), int(dr), (0,255,0))
            sx, sy = x, y
        else:
            instation = x > sbroi[0] and x < (sbroi[0]+sbroi[2]) and y < (sbroi[1]+sbroi[3]) and y > sbroi[1]
            if instation:
                stationary_status = 1
                sort_status = 0
                out_side_status = 0
                frame_stationary += 1
                cv2.circle(disp, (int(x),int(y)), int(dr), (0,255,0))
                count = counts.total_beads - 1
            else:
                stationary_status = 0
                sort_status = 0
                out_side_status = 1
                cv2.circle(disp, (int(x),int(y)), int(dr), (0,0,255)) 
         
        beads.data[counts.total_beads - 1, :] = [counts.total_beads, area, sort_status, stationary_status, out_side_status , x, y, counts.iframe, 0, 0]
         
    if frame_stationary == 1:
        counts.valid_frame += 1
        if frame_sort == 1:
            counts.sort_num += 1
            beads.data[count, 8:10] = [sx, sy]
        else:
            beads.data[count, 8:10] = [-1, -1]
#            if beads.data[count, 5] > 260 and beads.data[count, 5] < 275:
#                plt.figure()
#                plt.imshow(disp)
#                titlestr = 'frame ' + str(int(beads.data[count,7])) + ', (x,y) = (' + str(int(beads.data[count,5])) + ', ' + str(int(beads.data[count,6])) +'), inxex = ' + str(count)
#                plt.title(titlestr)
            
    return disp, counts, beads
    


def clean_up(cap, settings):
    if settings.general['RECORD'].value: settings.close_video()
    settings.general['RECORD'].value = False
    cap.release()
    cv2.destroyAllWindows()
    settings.save_settings()