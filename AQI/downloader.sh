periods=("2020" "2021Q1" "2021Q2" "2021Q3" "2021Q4" "2020Q1" "2020Q2" "2020Q3" "2020Q4" "2019Q1" "2019Q2" "2019Q3" "2019Q4" "2018H1" "2017H1" "2016H1" "2015H1")

echo periods are \"${periods[@]}
for period in "${periods[@]}"; do
	
	cmd="curl --compressed -o waqi-covid-$period.csv   https://aqicn.org/data-platform/covid19/report/36040-ac8df0d2/$period"
	echo $cmd
	eval $cmd
done
