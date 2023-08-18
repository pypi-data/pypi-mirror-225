# %%
from MDAnalysis import Universe
from MDContentAnalysis import TunnelAnalysis

#Save folder for all files
saveFolderPath = "data/analasys/FilReliansTest/Test2_Full/xtc"

#Load MD-system into Universe object
Uni = Universe("data/Component_top/short_md_c_sys.pdb", "data/short_md_center.xtc")

#Initiation analysis
analysis = TunnelAnalysis(Uni, saveFolderPath)

#Finding the tunnel
tunnels, tunnelFilters = analysis.tunnelAnalysis(protein=Uni.select_atoms('protein and not (name H*)'), 
                                                 start=[['A',112],['A',230],['A',343]], #S3 
                                                 end=[['B',586],['B',266],['B',261]], #BindingSight
                                                 hole2Filepath="~/Desktop/WORK/Programs/hole2/exe/hole",
                                                 random_seed=42)

#Analysing water content inside the tunnel
waterU = Uni.select_atoms('resname SOL')
waterIds, waterNum = analysis.contentAnalysis(waterU, ['OW', 'HW1', 'HW2'], 'water', False)
waterDistrebution  = analysis.atomPDF(waterIds)



#Ploting the water density distribution along the tunnel
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure(layout="constrained")
gs = plt.GridSpec(1, 1, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])

ax1.hist(waterDistrebution, range=(-10,50), bins=500, density=True)
ax1.set_xlabel('Length along tunnel direction [Å]', fontsize=16)
ax1.set_ylabel('PDF', fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=12)
plt.margins(0)
ax1.grid()

fig.suptitle('Water Distribution Along Tunnel', fontsize=20)
plt.show()


# %%
