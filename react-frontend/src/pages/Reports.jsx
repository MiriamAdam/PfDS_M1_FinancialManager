import React, {useEffect, useState} from "react";

/**
 * Returns an array of month names in German.
 * @returns {string[]} Array of month names ("January", "February", etc.)
 */
const getMonthNames = () => {
    return Array.from({ length: 12 }, (item, i) => {
        return new Date(null, i + 1, null).toLocaleDateString('de-DE', { month: 'long' });
    });
};

/**
 * Returns an array of the most recent 5 years including the current year.
 * @returns {number[]} Array of years (e.g., [2025, 2024, 2023, 2022, 2021])
 */
const getRecentYears = () => {
    const currentYear = new Date().getFullYear();
    const years = [];
    for (let i = 0; i < 5; i++) {
        years.push(currentYear - i);
    }
    return years;
};

/**
 * Reports component.
 *
 * Displays:
 * - A bar chart for monthly budget overview
 * - Donut charts for monthly spending and income shares
 * - Month and year selectors to update charts
 *
 * Fetches chart images from the backend and updates images on user selection.
 *
 * @component
 * @returns {JSX.Element} Rendered reports UI
 */
export default function Reports() {
    const [chartUrl, setChartUrl] = useState(null);
    const [monthlySpendingShareChartUrl, setMonthlySpendingShareChartUrl] = useState(null);
    const [monthlyIncomeShareChartUrl, setMonthlyIncomeShareChartUrl] = useState(null);
    const [monthNames, setMonthNames] = useState([]);
    const [availableYears, setAvailableYears] = useState([]);
    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();
    const [selectedMonth, setSelectedMonth] = useState(currentMonth);
    const [selectedYear, setSelectedYear] = useState(currentYear);

    /**
     * Initializes month names, recent years, and loads initial charts on mount.
     */
    useEffect(() => {
        setMonthNames(getMonthNames());
        setAvailableYears(getRecentYears());
        setChartUrl(`http://localhost:5000/api/chart/bar-chart?t=${Date.now()}`);
        reloadShareCharts(currentMonth, currentYear);
    }, []);

    /**
     * Reloads the monthly spending and income share charts for a given month and year.
     *
     * @param {number} month - Selected month (1-12)
     * @param {number} year - Selected year (e.g., 2025)
     */
    const reloadShareCharts = (month, year) => {
        const urlSpending = `http://localhost:5000/api/chart/monthly-spending-share-chart?year=${year}&month=${month}&t=${Date.now()}`;
        setMonthlySpendingShareChartUrl(urlSpending);
        const urlIncome = `http://localhost:5000/api/chart/monthly-income-share-chart?year=${year}&month=${month}&t=${Date.now()}`;
        setMonthlyIncomeShareChartUrl(urlIncome);
    }

    /**
     * Handles month selection change and reloads share charts.
     * @param {React.ChangeEvent<HTMLSelectElement>} e - Change event from month select
     */
     const handleMonthChange = (e) => {
        const month = parseInt(e.target.value, 10);
        setSelectedMonth(month);
        reloadShareCharts(month, selectedYear);
    }

    /**
     * Handles year selection change and reloads share charts.
     * @param {React.ChangeEvent<HTMLSelectElement>} e - Change event from year select
     */
    const handleYearChange = (e) => {
        const year = parseInt(e.target.value, 10);
        setSelectedYear(year);
        reloadShareCharts(selectedMonth, year);
    }

    return (
        <div className="flex flex-col items-center">
            {chartUrl && (
            <div className="bg-white pl-5 pt-5 pb-5 pr-5 mt-15 rounded-lg shadow-lg w-[80%]">
                <img
                    key={chartUrl}
                    src={chartUrl}
                    alt="monthly overview"
                    className="w-full max-w-3xl mx-auto"
                    crossOrigin="anonymous"
                />
            </div>
            )}
            <div className="flex flex-row gap-3 items-center bg-white p-3 pb-2 mt-10 mr-30 border-2 border-gray-200 rounded-2xl shadow-lg w-[25%]">
                <div className="flex flex-col flex-1">
                    <label htmlFor="month-select" className="text-center pr-3 text-sm font-medium text-gray-700 ">Month</label>
                    <select
                        id="month-select"
                        value={selectedMonth}
                        onChange={handleMonthChange}
                        className="mt-1 mb-5 block w-full rounded-md border-gray-300 shadow-sm"
                    >
                        {monthNames.map((monthName, index) => {
                            const monthValue = index + 1;
                            return (
                                <option key={monthName} value={monthValue}>{monthName}</option>
                            );
                        })}
                    </select>
                </div>
                <div className="flex flex-col flex-1">
                    <label htmlFor="year-select" className="text-center pr-3 text-sm font-medium text-gray-700 ">Year</label>
                     <select
                        id="year-select"
                        value={selectedYear}
                        onChange={handleYearChange}
                        className="mt-1 mb-5 block w-full rounded-md border-gray-300 shadow-sm"
                    >
                        {availableYears.map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>
                </div>
            </div>
            {monthlySpendingShareChartUrl && (
            <div className="bg-white pl-5 pt-5 pb-5 pr-5 mt-3 rounded-lg shadow-lg w-[80%]">
                <img
                    key={monthlySpendingShareChartUrl}
                    src={monthlySpendingShareChartUrl}
                    alt="monthly overview"
                    className="w-full max-w-3xl mx-auto"
                    crossOrigin="anonymous"
                />
            </div>
            )}
             {monthlyIncomeShareChartUrl && (
            <div className="bg-white pl-5 pt-5 pb-5 pr-5 mt-3 mb-10 rounded-lg shadow-lg w-[80%]">
                <img
                    key={monthlyIncomeShareChartUrl}
                    src={monthlyIncomeShareChartUrl}
                    alt="monthly overview"
                    className="w-full max-w-3xl mx-auto"
                    crossOrigin="anonymous"
                />
            </div>
            )}
        </div>
    )
}