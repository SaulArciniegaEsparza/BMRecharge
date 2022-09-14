# BMRecharge - Basin of Mexico Recharge App

**Groundwater recharge** is a complex variable to underestand that depends on multiple factors including climatology, vegetation, topography, soil properties, and surficial geology, among others.

Groundwater recharge estimates are essential to improve water management practices in the so-called **Basin of Mexico**, an ~8,800 km$^{2}$ basin in central Mexico where groundwater abstraction exceeds natural recharge from rainfall percolation, leading to increasing drawdown rates, hydrogeochemical degradation and severe land subsidence.

The **BMRecharge-App** is a Web-based explorer tool to visualize, display, assess, and download the **annual potential recharge** modeled across the Basin of Mexico for the period 2000-2021. Overall, quantitative evaluation of groundwater resources in the Basin of Mexico is of prime interest in our research Group (the **Hydrogeology Group** at the [**Faculty of Engineering, UNAM**](https://www.ingenieria.unam.mx/index.php), Mexico), and currently, the analysis of potential recharge in this basin represents the PhD research topic of [*Sergio Gonzalez-Ortigoza*](https://www.linkedin.com/in/sergio-gonzalez-ortigoza-47a97024a/). 


## Instructions

1. From the left side panel, select the **data type**, namely, how to visualize the modeled recharge in the Basin of Mexico: by aquifer or groundwater management unit (**Aquifers**), by geographical zones (**Zones**), or as a gridded-based continuous domain (**Basin-wide**). If "About" is selected, you will be returned to this page.

2. Different climatological databases were used to simulate recharge to evaluate the impact of different data sources. After the data type is selected, choose the desired database:

    - *Ground Gauges*: Climatological data from ground stations considering the period 2000-2016 from the [**Mexican Meteorological Service (SMN)**](https://smn.conagua.gob.mx/es/climatologia/informacion-climatologica/informacion-estadistica-climatologica). The daily precipitation and temperature was interpolated to force the model.
    - *CHIRPS*: Remotely-sensed global daily precipitation from the [Climate Hazards Group InfraRed Precipitation with Station data](https://www.chc.ucsb.edu/data/chirps) (*Funk et al., 2015*), in combination with daily air temperature from the [**SMN**](https://smn.conagua.gob.mx/es/climatologia/informacion-climatologica/informacion-estadistica-climatologica) ( period 2000-2016).
    - *CHIRPSC*: A bias corrected version of the [CHIRPS](https://www.chc.ucsb.edu/data/chirps) product using ground stations in combination with daily air temperature from the [**SMN**](https://smn.conagua.gob.mx/es/climatologia/informacion-climatologica/informacion-estadistica-climatologica) (period 2000-2016).
    - *CHIRPS-Daymet*: Daily precipitation from [CHIRPS](https://www.chc.ucsb.edu/data/chirps) and daily air temperature from the global gridded product [**Daymet**](https://daymet.ornl.gov/) from the NASA (period 2000 to 2021).

3. Select a color gradient to better visualize the spatial variability of the potential recharge in the Basin of Mexico.


## About the model

The potential recharge in the Basin of Mexico was modeled using the [**Soil Water Balance**](https://www.usgs.gov/centers/upper-midwest-water-science-center/science/soil-water-balance-swb-modified-thornthwaite#overview) model, a distributed model that calculates components of the water balance at a daily time-step by means of a modified version of the Thornthwaite-Mather soil-moisture-balance approach (*Thornthwaite and Mather, 1957*). The SWB Model 2.0 was used (Westenbroek et al., 2018), which is the evolution of the soil water balance model developed by *Dripps and Bradbury (2007)* and has been improved to facilitate data input and net infiltration modeling.


## About the authors

**Recharge Modeler**: *Sergio González-Ortigoza*, PhD. candidate at the [**Programa de Maestria y Doctorado en Ingenieria Civil, UNAM**](http://ingen.posgrado.unam.mx/). Social Media: [**LinkedIn**](https://www.linkedin.com/in/sergio-gonzalez-ortigoza-47a97024a/)

**App Developer**: *Dr. Saul Arciniega-Esparza*, Full Time Associate Professor at the [**Faculty of Engineering, UNAM**](https://www.ingenieria.unam.mx/index.php). Member of the [**Hydrogeology Group**](https://www.ingenieria.unam.mx/hydrogeology/). Social Media: [**ResearchGate**](https://www.researchgate.net/profile/Saul-Arciniega-Esparza) | [**Twitter**](https://twitter.com/zaul_arciniega) | [**LinkedIn**](https://www.linkedin.com/in/saularciniegaesparza/)

**Principal Researcher**: *Dr. Antonio Hernández-Espriú*, Full Time Research Professor at the [**Faculty of Engineering, UNAM**](https://www.ingenieria.unam.mx/index.php). Leader of the [**Hydrogeology Group**](https://www.ingenieria.unam.mx/hydrogeology/). Social Media: [**ResearchGate**](https://www.researchgate.net/profile/Antonio-Hernandez-Espriu) | [**Twitter**](https://twitter.com/hydrogeologymx).


## References

Dripps WR, Bradbury KR (2007) A simple daily soil-water balance model for estimating the spatial and temporal distribution of groundwater recharge in temperate humid areas, Hydrogeology J. 15(3), 433–444, [https://doi.org/10.1007/s10040-007-0160-6](https://doi.org/10.1007/s10040-007-0160-6)

Funk C, Peterson P, Landsfeld M, Pedreros D, Verdin J, Shukla S, Husak G, Rowland J, Harrison L, Hoell A, et al. 2015. The climate hazards infrared precipitation with stations - A new environmental record for monitoring extremes. Scientific Data 2: 1–21 DOI: [10.1038/sdata.2015.66](https://www.nature.com/articles/sdata201566)

Thornthwaite CW, Mather JR (1957) Instructions and tables for computing potential evapotranspiration and the water balance. Publ Climatol 10(3).

Westenbroek SM, Engott JA, Kelson VA, Hunt RJ (2018) SWB Version 2.0 - A Soil-Water-Balance Code for Estimating Net Infiltration and Other Water-Budget Components, U.S. Geol. Surv., (Techniques and Methods 6-A59), 118, [https://pubs.usgs.gov/tm/06/a59/tm6a59.pdf](https://pubs.usgs.gov/tm/06/a59/tm6a59.pdf)

