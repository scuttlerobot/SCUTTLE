function varargout = GUI_MXET300(varargin)
%GUI_MXET300 MATLAB code file for GUI_MXET300.fig
%      GUI_MXET300, by itself, creates a new GUI_MXET300 or raises the existing
%      singleton*.
%
%      H = GUI_MXET300 returns the handle to a new GUI_MXET300 or the handle to
%      the existing singleton*.
%
%      GUI_MXET300('Property','Value',...) creates a new GUI_MXET300 using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to GUI_MXET300_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      GUI_MXET300('CALLBACK') and GUI_MXET300('CALLBACK',hObject,...) call the
%      local function named CALLBACK in GUI_MXET300.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI_MXET300

% Last Modified by GUIDE v2.5 22-Aug-2018 12:40:51

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @GUI_MXET300_OpeningFcn, ...
    'gui_OutputFcn',  @GUI_MXET300_OutputFcn, ...
    'gui_LayoutFcn',  [], ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI_MXET300 is made visible.
function GUI_MXET300_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for GUI_MXET300
handles.output = hObject;

% --- ADD Variables (e.g. user input/data/udp_object/..)
handles.state = true;
handles.connection_status = 0; %0: no conn. 1:conn. 2: maybe
handles.AxesPlot = plot(handles.AxesData, [0] );
set(handles.AxesData.YLabel, 'String', 'Speed (m/s)');
set(handles.AxesData.Title, 'String', 'Speed (m/s)')
set(handles.AxesData, 'XLim', [-5 5])
set(handles.AxesData, 'YLim', [-5 5])

% legend('angle', 'x', 'y')
% user inputs
handles.ip = '192.168.8.1';
handles.udpPort = 3553;
handles.drop_count = 0; % dropped packets
handles.BBB_data = zeros(1,13);
handles.sliderSpeedL = 100; % max speed
handles.sliderSpeedR = 100;
handles.arrowUp = 0;
handles.arrowDown = 0;
handles.arrowLeft = 0;
handles.arrowRight = 0;
% sensors
handles.distance = 0;
handles.speedSensorL = 0;
handles.speedSensorR = 0;
handles.encoderL = 0;
handles.encoderR = 0;
handles.compass = 0;
handles.pitch = 0;
handles.roll = 0;
handles.hBridgeTempL = 0;
handles.hBridgeTempR = 0;
handles.hBridgeVoltageL = 0;
handles.hBridgeVoltageR = 0;
% slider listeners
addlistener(handles.SliderRightSpeed,'Value', 'PostSet',@(src,event) ...
    set(handles.TextRightSpeed, 'String', ...
    uint16(get(handles.SliderRightSpeed,'Value'))));
addlistener(handles.SliderLeftSpeed,'Value', 'PostSet',@(src,event) ...
    set(handles.TextLeftSpeed, 'String', ...
    uint16(get(handles.SliderLeftSpeed,'Value'))));
% Update handles structure
guidata(hObject, handles);

%delete the stupid arrow
delete(findall(hObject,'type','annotation'))
%draw compass and edit
fix_compass_axes(handles)
lineLength = 0.05;
x(1) = 0.435;
y(1) = 0.85;
angle = 90;
% this is relative, x:y ratio of graph (window size) is 2:1
x(2) = x(1) + lineLength * cosd(angle);
y(2) = y(1) + 2*lineLength * sind(angle);
handles.annot = annotation(handles.fig,'arrow',x, y,...
    'Color','k',...
    'LineWidth',3);

% UIWAIT makes GUI_MXET300 wait for user response (see UIRESUME)
% uiwait(handles.figure1);

% remove axes x/y and redraw circle labels
function [] = fix_compass_axes(handles)
axes(handles.AxesCompass)
h_fake=compass(0);
% the next line is to avoid "resizing" the axes when the view is changed
handles.AxesCompass.CameraViewAngleMode = 'manual';
view(-90,90)
labels = findall(handles.AxesCompass,'type','text');
a=findall(handles.AxesCompass, 'String', '0', '-or','String','180',...
    '-or','String','90','-or','String','270');
view(-90,90)
set(labels,'visible','off');
set(a,'visible','on');
set(findall(handles.AxesCompass, 'String', '0'),'String', 'N',...
    'FontSize', 14);
set(findall(handles.AxesCompass, 'String', '180'),'String', 'S',...
    'FontSize', 14);
set(findall(handles.AxesCompass, 'String', '90'),'String', 'W',...
    'FontSize', 14);
set(findall(handles.AxesCompass, 'String', '270'),'String', 'E',...
    'FontSize', 14);

% --- Outputs from this function are returned to the command line.
function varargout = GUI_MXET300_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;





% Hints: get(hObject,'String') returns contents of TextLeftSpeed as text
%        str2double(get(hObject,'String')) returns contents of TextLeftSpeed as a double


function TextIP_Callback(hObject, eventdata, handles)
% hObject    handle to TextIP (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str= (get(hObject,'String'));
if ~all(ismember(str, '.1234567890'))
    set(hObject,'string',handles.ip);
    warndlg('Input must be numerical (integer)');
else
    handles.ip = str;
end
guidata(hObject, handles);

% Hints: get(hObject,'String') returns contents of TextIP as text
%        str2double(get(hObject,'String')) returns contents of TextIP as a double


function TextUDPPort_Callback(hObject, eventdata, handles)
% hObject    handle to TextUDPPort (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str= (get(hObject,'String'));
if ~all(ismember(str, '1234567890'))
    set(hObject,'string',handles.udpPort);
    warndlg('Input must be a number between 1023 and 65535');
else
    handles.udpPort = str2num(str);
end
guidata(hObject, handles);

% Hints: get(hObject,'String') returns contents of TextUDPPort as text
%        str2double(get(hObject,'String')) returns contents of TextUDPPort as a double

% --- Executes on slider movement.
function SliderRightSpeed_Callback(hObject, eventdata, handles)
% hObject    handle to SliderRightSpeed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.sliderSpeedR = get(hObject,'Value');
guidata(hObject, handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes on slider movement.
function SliderLeftSpeed_Callback(hObject, eventdata, handles)
% hObject    handle to SliderLeftSpeed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.sliderSpeedL = get(hObject,'Value');
guidata(hObject, handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider




% --- Executes on button press in BtnConnect.
function BtnConnect_Callback(hObject, eventdata, handles)
% hObject    handle to BtnConnect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% close connections if previously open
snew = instrfind;
if (~isempty(snew))
    for inst = snew
        if strfind(inst.Name,handles.ip)
            fclose(inst);
        end
    end
end
% create and open UDP/IP object
handles.UDPObject = udp(handles.ip, handles.udpPort);
handles.UDPObject.InputBufferSize = 2^10;
handles.UDPObject.ByteOrder = 'littleEndian';
handles.UDPObject.Timeout = 1e-3;
handles.UDPObject.BytesAvailableFcnMode = 'byte';
handles.UDPObject.BytesAvailableFcnCount = 20;
handles.UDPObject.BytesAvailableFcn = {@Update_data, handles} ;

guidata(hObject, handles);
% open the UDP/IP object
fopen(handles.UDPObject);
Send_UDP(handles,0)


% --- Executes on key press with focus on fig and none of its controls.
function fig_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to fig (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
switch eventdata.Key
    case 'uparrow'
        set(handles.BtnArrowUp, 'ForegroundColor','r')
        BtnArrowUp_ButtonDownFcn(handles.BtnArrowUp, eventdata, handles);
    case 'downarrow'
        set(handles.BtnArrowDown, 'ForegroundColor','r')
        BtnArrowDown_ButtonDownFcn(handles.BtnArrowDown, eventdata, handles);
    case 'leftarrow'
        set(handles.BtnArrowLeft, 'ForegroundColor','r')
        BtnArrowLeft_ButtonDownFcn(handles.BtnArrowLeft, eventdata, handles);
    case 'rightarrow'
        set(handles.BtnArrowRight, 'ForegroundColor','r')
        BtnArrowRight_ButtonDownFcn(handles.BtnArrowRight, eventdata, handles);
    otherwise
        Send_UDP(handles, eventdata.Key)
end


% --- Executes on key release with focus on fig and none of its controls.
function fig_KeyReleaseFcn(hObject, eventdata, handles)
% hObject    handle to fig (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	Key: name of the key that was released, in lower case
%	Character: character interpretation of the key(s) that was released
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) released
% handles    structure with handles and user data (see GUIDATA)

% --- do not catch input if inside text
current_focus = gco;
try
    if (current_focus.Style == 'edit')
        if current_focus.Enable == 'on'
            return
        end
    end
end
% ---
switch eventdata.Key
    case 'uparrow'
        set(handles.BtnArrowUp, 'ForegroundColor',[0 0 0] )
        BtnArrowUp_Callback(handles.BtnArrowUp, eventdata, handles);
    case 'downarrow'
        set(handles.BtnArrowDown, 'ForegroundColor',[0 0 0] )
        BtnArrowDown_Callback(handles.BtnArrowDown, eventdata, handles);
    case 'leftarrow'
        set(handles.BtnArrowLeft, 'ForegroundColor',[0 0 0] )
        BtnArrowLeft_Callback(handles.BtnArrowLeft, eventdata, handles);
    case 'rightarrow'
        set(handles.BtnArrowRight, 'ForegroundColor',[0 0 0] )
        BtnArrowRight_Callback(handles.BtnArrowRight, eventdata, handles);
    case 'p'
        if handles.state
            handles.mapDim = get(handles.AxesData , 'outerposition');
            set(findall(hObject, '-property', 'Visible'), 'Visible', 'off')
            set(handles.fig, 'Visible', 'on')
            set(handles.AxesData, 'Visible', 'on')
            commandwindow
            figure(handles.fig)
            set(handles.AxesData, 'Units', 'normalized','position',[0.05 0.05 0.9 0.9])
            set(get(handles.AxesData,'children'),'visible','on')
            handles.state = false;
        else
            set(handles.AxesData , 'Units', 'normalized','outerposition',handles.mapDim)
            set( findall(hObject,'-property', 'Visible'), 'Visible', 'on')
            fix_compass_axes(handles)
            handles.state = true;
        end
        guidata(hObject, handles);
    otherwise
        Send_UDP(handles, 0)
        % --- clean up
        %     case 'a'
        %         fprintf('right %d\n',handles.arrowRight)
        %         fprintf('down %d\n',handles.arrowDown)
end






% --- Executes when user attempts to close fig.
function fig_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to fig (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
try
    fclose(handles.UDPObject);
    delete(handles.UDPObject);
    
catch
    fprintf('No UDP \n')
end

delete(hObject);


function TextRightSpeed_Callback(hObject, eventdata, handles)
% hObject    handle to TextRightSpeed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str= (get(hObject,'String'));
if ~all(ismember(str, '1234567890'))
    set(hObject,'string','0');
    warndlg('Input must be numerical (integer)');
elseif (uint16(str2num(str)) > 100)
    warndlg('Speed range is 0-100 ');
    %set(hObject,'string',handles.sliderSpeedR);
    %handles.sliderSpeedR = 100;
elseif str2num(str) < 0
    warndlg('Speed range is 0-100 ');
    %set(hObject,'string',handles.sliderSpeedR);
    %handles.sliderSpeedR = 0;
else
    handles.sliderSpeedR = str2num(str);
end
set(hObject,'string',handles.sliderSpeedR);
set(handles.SliderRightSpeed, 'Value', handles.sliderSpeedR)
guidata(hObject, handles);

% Hints: get(hObject,'String') returns contents of TextRightSpeed as text
%        str2double(get(hObject,'String')) returns contents of TextRightSpeed as a double


function TextLeftSpeed_Callback(hObject, eventdata, handles)
% hObject    handle to TextLeftSpeed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str= (get(hObject,'String'));
if ~all(ismember(str, '1234567890'))
    set(hObject,'string','0');
    warndlg('Input must be numerical (integer)');
elseif (uint16(str2num(str)) > 100)
    warndlg('Speed range is 0-100 ');
    %set(hObject,'string',handles.sliderSpeedL);
    %handles.sliderSpeedR = 100;
elseif str2num(str) < 0
    warndlg('Speed range is 0-100 ');
    %set(hObject,'string',handles.sliderSpeedL);
    %handles.sliderSpeedR = 0;
else
    handles.sliderSpeedL = str2num(str);
end
set(hObject,'string',handles.sliderSpeedL);
set(handles.SliderLeftSpeed, 'Value', handles.sliderSpeedL)
guidata(hObject, handles);


% --- Executes on button press in BtnArrowLeft.
function BtnArrowLeft_Callback(hObject, eventdata, handles)
% hObject    handle to BtnArrowLeft (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowLeft = 0;
guidata(hObject, handles);
Send_UDP(handles,0)




% --- Executes on button press in BtnArrowDown.
function BtnArrowDown_Callback(hObject, eventdata, handles)
% hObject    handle to BtnArrowDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowDown = 0;
guidata(hObject, handles);
Send_UDP(handles,0)


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over BtnArrowUp.
function BtnArrowUp_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to BtnArrowUp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowUp=1;
guidata(hObject, handles);
Send_UDP(handles,0)



% --- Executes on button press in BtnArrowUp.
function BtnArrowUp_Callback(hObject, eventdata, handles)
% hObject    handle to BtnArrowUp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowUp = 0;
guidata(hObject, handles);
Send_UDP(handles,0)



% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over BtnArrowLeft.
function BtnArrowLeft_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to BtnArrowLeft (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowLeft = 1;
guidata(hObject, handles);
Send_UDP(handles,0)


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over BtnArrowDown.
function BtnArrowDown_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to BtnArrowDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowDown = 1;
guidata(hObject, handles);
Send_UDP(handles,0)

% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over BtnArrowRight.
function BtnArrowRight_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to BtnArrowRight (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowRight = 1;
guidata(hObject, handles);
Send_UDP(handles,0)

% --- Executes on button press in BtnArrowRight.
function BtnArrowRight_Callback(hObject, eventdata, handles)
% hObject    handle to BtnArrowRight (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.arrowRight = 0;
guidata(hObject, handles);
Send_UDP(handles,0)


function handles = Update_data(hObject, eventdata, handles)
% fprintf('bytes available callback (count=%i)\n',hObject.BytesAvailable)
hFig = findall(0,'name','MXET 300 Control Panel');
handles = guidata(hFig);
handles = Get_UDP(handles);
Update_Graph(handles);
Update_Fields(handles);
guidata(handles.fig, handles);
drawnow


function Send_UDP(handles,timer)
u = handles.arrowUp;
d = handles.arrowDown;
l = handles.arrowLeft;
r = handles.arrowRight;
maxL = handles.sliderSpeedL/100.0*127.0;
maxR = handles.sliderSpeedR/100.0*127.0;
speedL = uint8(127+maxL*(1-l)*((u+r)>0)  + maxL/2*(u*l) - maxL*(d)*(1-l) ...
    - maxL/2*(d*l) -maxL*d*r);
speedR = uint8(127+maxR*(1-r)*((u+l)>0)  + maxR/2*(u*r) - maxR*(d)*(1-r) ...
    - maxR/2*(d*r) -maxR*d*l);
try
    fwrite(handles.UDPObject, [speedL, speedR, timer])
catch ME
    switch ME.identifier
        case 'MATLAB:nonExistentField'
            fprintf('no UDP connection\n')
        otherwise
            fprintf('something wrong with UDP connection\n')
    end
end

function handles = Get_UDP(handles)
[data_in,count,warn_msg] =fread(handles.UDPObject,32,'float');
% fprintf('Get_UDP (count=%i)\n',handles.UDPObject.BytesAvailable)
if warn_msg
    if (handles.connection_status ~= 0)
        handles.drop_count = handles.drop_count + 1;
        fprintf('Dropped packet (counter: %d) \n', handles.drop_count)
        set(handles.ConnStat, 'String', 'ON', 'ForegroundColor',[1,165/265,0])
        handles.connection_status = 2;
    end
else
    handles.connection_status = 1;
    handles.drop_count = (handles.drop_count - 1)*(handles.drop_count>0);
    set(handles.ConnStat, 'String', 'ON', 'ForegroundColor','green')
    handles.BBB_data = [handles.BBB_data; data_in'];
end
if (handles.drop_count >=10)
    handles.connection_status = 0;
    warndlg('seems connection is lost')
    handles.drop_count = 0;
    set(handles.ConnStat, 'String', 'OFF', 'ForegroundColor','Red')
end

function Update_Graph(handles)
i = 7;
j = 8;
% angle: 1;
% x: 4;
% y: 5;

angle = handles.BBB_data(end, 1);
% updates compass orientation 
handles.AxesCompass.View=[-90-angle,90];  % [180+angle,90]
% updates data plot (chart)
set(handles.AxesPlot, 'YData', handles.BBB_data(:,j))
set(handles.AxesPlot, 'XData', handles.BBB_data(:,i))


% drawnow limitrate

function Update_Fields(handles)
handles.pitch = handles.BBB_data(end, 12);
handles.roll = handles.BBB_data(end, 13);
handles.hBridgeVoltageL = handles.BBB_data(end, 2);
handles.hBridgeVoltageR = handles.BBB_data(end, 3);
handles.hBridgeTempL = handles.BBB_data(end, 4);
handles.hBridgeTempR = handles.BBB_data(end, 5);
handles.distance = handles.BBB_data(end, 11);
handles.encoderL = handles.BBB_data(end, 7);
handles.encoderR = handles.BBB_data(end, 8);
handles.speedSensorL = handles.BBB_data(end, 9);
handles.speedSensorR = handles.BBB_data(end, 10);
set(handles.TextSensorPitch, 'String', round(handles.pitch,2))
set(handles.TextSensorRoll, 'String', round(handles.roll,2))
set(handles.TextSensorDistance, 'String', round(handles.distance,2))
set(handles.TextSensorSpeedLeft, 'String', round(handles.speedSensorL,2))
set(handles.TextSensorSpeedRight, 'String', round(handles.speedSensorR,2))
set(handles.TextSensorEncoderLeft, 'String', round(handles.encoderL,2))
set(handles.TextSensorEncoderRight, 'String', round(handles.encoderR,2))
set(handles.TextSensorTempLeft, 'String', round(handles.hBridgeTempL,2))
set(handles.TextSensorTempRight, 'String', round(handles.hBridgeTempR,2))
set(handles.TextSensorVoltageLeft, 'String', round(handles.hBridgeVoltageL,2))
set(handles.TextSensorVoltageRight, 'String', round(handles.hBridgeVoltageR,2))

if handles.hBridgeVoltageL < 12
   set(handles.TextSensorVoltageLeft, 'ForegroundColor','Red')
end
guidata(handles.fig, handles);
