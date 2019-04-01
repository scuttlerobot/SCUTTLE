%% EXAMPLE: Differential Drive discrete simulation
% Modified by David Malawey, Dec 2018
% This program started with mrsDiffDriveDiscrete.m and was defined for
% SCUTTLE parameters, with additional comments added for students to
% understand.

%% Define Robot
R = 0.084;                % Wheel radius [m]
L = 0.402;                % Wheelbase [m]
dd = DifferentialDrive(R,L);

%% Simulation parameters
sampleTime = 0.01;              % Sample time [s]
initPose = [0;0;pi/4];          % Initial pose (x y theta)

% Initialize time, input, and pose arrays
tVec = 0:sampleTime:10;         % Time array
vRef = 0.2*ones(size(tVec));    % Reference linear speed
wRef = zeros(size(tVec));       % Reference angular speed
wRef(tVec < 5) = -0.5;          % assign angular velocity for first 5 seconds (positive)
wRef(tVec >=5) = -0.95;           % assign angular velocity for second 5 seconds (negative)
pose = zeros(3,numel(tVec));    % Pose matrix (3 rows by number-of-elements columns)
pose(:,1) = initPose;           % reassign pose for first column to be initial pose  

%% Simulation loop
for idx = 2:numel(tVec)   % index is 1-row by 1001 columns.  For-loop will execute 1000 times.
    % Solve inverse kinematics to find wheel speeds
    [wL,wR] = inverseKinematics(dd,vRef(idx-1),wRef(idx-1));% (dd,0.2,0.5);
    
    % Compute the velocities
    [v,w] = forwardKinematics(dd,wL,wR);
    velB = [v;0;w]; % Body velocities [vx;vy;w]
    vel = bodyToWorld(velB,pose(:,idx-1));  % Convert from body to world
    
    % Perform forward discrete integration step
    pose(:,idx) = pose(:,idx-1) + vel*sampleTime;         
end

%% Display results
close all
figure
hold on
plot(pose(1,1),pose(2,1),'ro', ...     %starting point (red circle)
     pose(1,end),pose(2,end),'go', ... %ending point (green circle)
     pose(1,:),pose(2,:),'b-');        %full trajectory in blue line
axis equal
title('Vehicle Trajectory');
xlabel('X [m]')
ylabel('Y [m]')
legend('Start','End','Trajectory')