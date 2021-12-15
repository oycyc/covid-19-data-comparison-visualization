# COVID-19 Comparison Graph Generator

A simple program with a GUI that generates a graph comparing two U.S. states. The options include line, bar, and pie charts. The output can be animated or just an image file.

There are four metric types: 

- Total Cumulative COVID-19 Cases
- Daily New COVID-19 Cases (Rolling Avg. of 7 Days)
- Total Cumulative COVID-19 Deaths
- Daily New COVID-19 Deaths (Rolling Avg. of 7 Days)

### Usage

Run `gui.py` to open the GUI. Choose from the available options and the generated graph will be a in the corresponding  `/graphs` folder.

### Demo

<p align="center"><img src="assets/demo.gif" width="65%" height="65%" alt="Demonstration"></p>
<p align="center"><img src="assets/gui_demo.png" width="40%" height="40%" alt="GUI Demonstration Picture"></p>
<p align="center">
	<img src="graphs/bar_chart/20_30-12-14-21AlabamaVsWashington_DailyNewCases(RollingAvg.).gif" width="45%" height="45%" alt="Graph Example">
	<img src="graphs/line_chart/21_53-12-14-21CaliforniaVsNewJersey_DailyNewDeaths(RollingAvg.).gif" width="45%" height="45%" alt="Graph Example">
</p>
<p align="center">
	<img src="graphs/line_chart/08_07-12-15-21ArkansasVsVermont_Daily New Deaths (Rolling Avg.).png" width="45%" height="45%" alt="Graph Example">
	<img src="graphs/pie_chart/11_00-12-15-21NewYorkVsNewJersey_Total Cumulative Cases.png" width="45%" height="45%" alt="Graph Example">
</p>
#### All examples are in `/graphs` folder.

