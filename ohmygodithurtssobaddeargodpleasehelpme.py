import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# latitudes = ["005","050"]
latitude = "005"  # 005: near equator; 050: midlatitude

pressures = ["650", "700", "725"]  # in hPa

yearmonth = "200901"
dates = [f"{i:02d}" for i in range(5, 17, 1)]  # from Jan 5th to 16th
hours = ["03", "09", "15", "21"]

quantities = ["u", "v", "omega", "T", "Z", ]

path2file = "C:\\Users\\Ander\\Documents\\data\\"  # directory to data files

data = {}
# for latitude in latitudes: just do separate for different latitudes
for quantity in quantities:
    q_array = np.zeros((len(dates) * len(hours), 3, 3, len(pressures)))
    for ip, pressure in enumerate(pressures):
        for id_, date in enumerate(dates):
            for ih, hour in enumerate(hours):
                # filename = "KH.Y005.P650.2009010503.2.dat"
                filename = (
                    f"{quantity}.Y{latitude}.P{pressure}.{yearmonth}{date}{hour}.dat"
                )

                with open(path2file + filename, "r") as f:
                    array = np.loadtxt(f)
                q_array[len(hours) * id_ + ih, :, :, ip] = array[1:, 1:]

                if quantity == quantities[0]:  # saving lat, lon only needs to be done once
                    lat = array[1:, 0]
                    lon = array[0, 1:]
                    data["lat"] = lat
                    data["lon"] = lon
    data[quantity] = q_array

# Conversion to SI units

deg2rad = np.pi / 180

data["lat"] *= deg2rad  # degree -> radian
data["lon"] *= deg2rad  # degree -> radian

data["pressure"] = np.array(pressures, dtype=float) * 100  # hPa -> Pa

hr2sec = 3600

data["time"] = np.linspace(0, 6 * data["u"].shape[0], data["u"].shape[0]) * hr2sec  # hour -> second

# Calculate U-Momentum Terms for Midlatitudes
# Add your U-Momentum calculations here

Om = 2*np.pi/24/3600 # Earth's rotation
g = 10 # surface gravity
a = 6.4e6 # Earth's radius

R = 287 # gas constant

# x-momentum equation, for all times and for all pressures
def xmom(data):
    phi = data["lat"][1]
    dx = (data["lon"][2] - data["lon"][0])*a*np.cos(phi) # dx = a*cos phi * 0.635 degrees
    dy = (data["lat"][2] - data["lat"][0])*a # dy = a * .5 degrees
    dt = data["time"][2] - data["time"][0] # dt = 12 hours
    
    terms = np.zeros((9,len(data["time"])-2,len(data["pressure"])-2))
    for ind_p in range(1,len(data["pressure"])-1):
        p = data["pressure"][ind_p]
        dp = data["pressure"][ind_p+1] - data["pressure"][ind_p-1]
        for ind_t in range(1,len(data["time"])-1):
            u = data["u"][ind_t,1,1,ind_p]
            v = data["v"][ind_t,1,1,ind_p]
            om = data["omega"][ind_t,1,1,ind_p]
            T = data["T"][ind_t,1,1,ind_p]
            rho = p/R/T
            
            # -1 after index for saving because the indices start from 1
            terms[0,ind_t-1,ind_p-1] = (data["u"][ind_t+1,1,1,ind_p] - data["u"][ind_t-1,1,1,ind_p]) / dt  # du/dt 
            terms[1,ind_t-1,ind_p-1] = u*(data["u"][ind_t,1,2,ind_p] - data["u"][ind_t,1,0,ind_p]) / dx  # u*du/dx
            terms[2,ind_t-1,ind_p-1] = v*(data["u"][ind_t,2,1,ind_p] - data["u"][ind_t,0,1,ind_p]) / dy  # v*du/dy
            terms[3,ind_t-1,ind_p-1] = om*(data["u"][ind_t,1,1,ind_p+1] - data["u"][ind_t,1,1,ind_p-1]) / dp  # omega*du/dp
            terms[4,ind_t-1,ind_p-1] = - u*v*np.tan(phi)/a  # u*v*tan(phi)/a
            terms[5,ind_t-1,ind_p-1] = - u*om/(rho*g*a)  # u*om/rho*g*a
            terms[6,ind_t-1,ind_p-1] = - g*(data["Z"][ind_t,1,2,ind_p] - data["Z"][ind_t,1,0,ind_p]) / dx  # g*dz/dx
            terms[7,ind_t-1,ind_p-1] = 2*Om*v*np.sin(phi)  # 2*Om*v*sin(phi)
            terms[8,ind_t-1,ind_p-1] = 2*Om*om/(rho*g)*np.cos(phi)  # 2*Om*om/(rho*gz0)*cos(phi)

    return terms

terms = xmom(data)

# Generate a list of distinct colors for each line
colors = plt.cm.viridis(np.linspace(0, 1, len(terms)))

fig, ax = plt.subplots(facecolor='black')  # Set background color to black
ax.set_facecolor('black')  # Set axes background color to black

for ind_term, term in enumerate(terms[:, :, 0]):
    label = fr"term{ind_term + 1:d}"  # Label for each line
    ax.plot(data["time"][1:-1], np.abs(term), marker='^', label=label, color=colors[ind_term])

ax.set_yscale("log")
ax.set_xlabel("time [s]", color='white')  # Set label text color to white
ax.set_ylabel("magnitude [m/s$^2$]", color='white')  # Set label text color to white

# Set tick colors to white
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.grid(color='white', linestyle='--', linewidth=0.5)  # Set grid color to white

# Move legend to the right outside the plot area
ax.legend(facecolor='black', edgecolor='white', loc='center left', bbox_to_anchor=(1, 0.5), title="Legend", labelcolor='white')

ax.set_title("U-momentum Equation Terms \nfor Tropics", color='white')  # Set title text color to white

plt.show()
