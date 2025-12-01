clear;

%% constants
hbar = 6.626e-34/2/pi;
e = 1.6e-19;
m = 9.1e-31;
mu_b = e/2/m*hbar;

%% path to file
to_plot = '2024-10-30_RT_ESRes4_hf-s20-f3_S12.csv';
delimiter = ',';
headerlines = 0;

%% get data
data_to_plot = importdata(to_plot, delimiter, headerlines);

f = data_to_plot(:,1)./1e9;
mag = data_to_plot(:,2);
phase = data_to_plot(:,3);

%% plot

fmag = figure(1);
plot(f,mag)
xlabel('Frequency (GHz)')
ylabel('Magnitude (dB)')
fmag.Position = [50,600,560/1.2,420/1.2];

fphase = figure(2);
plot(f,phase)
xlabel('Frequency (GHz)')
ylabel('Phase (deg)')
fphase.Position = [50,150,560/1.2,420/1.2];
