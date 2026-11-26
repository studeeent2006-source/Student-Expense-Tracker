
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", Arial, sans-serif;
    background: #F4F5FA;
    color: #252B42;
}

/* Sidebar */

.sidebar {
    width: 220px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    background: #202744;
    padding: 35px 20px;
    color: white;
}

.sidebar h2 {
    font-size: 23px;
    line-height: 1.4;
    margin-bottom: 8px;
}

.sidebar h2 span {
    color: #A99FFF;
}

.side-label {
    color: #858BA3;
    font-size: 11px;
    margin: 30px 10px 15px;
    letter-spacing: 1px;
}

.sidebar a {
    display: block;
    text-decoration: none;
    color: #E0E3F0;
    padding: 13px 12px;
    margin: 6px 0;
    border-radius: 8px;
    transition: 0.2s;
}

.sidebar a:hover {
    background: #343D61;
    color: white;
}

.side-footer {
    position: absolute;
    bottom: 25px;
    color: #B8BED5;
    font-size: 12px;
}

/* Main content */

.main-content {
    margin-left: 220px;
    padding: 30px;
    max-width: 1600px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

header h1 {
    font-size: 27px;
}

header p {
    color: #858BA3;
    margin-top: 5px;
}

.date {
    color: #7565D9;
    font-weight: bold;
}

/* Summary cards */

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 22px;
}

.card {
    background: white;
    padding: 23px;
    border-radius: 13px;
    box-shadow: 0 4px 15px rgba(30, 35, 65, 0.04);
}

.card p {
    color: #858BA3;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
}

.card h2 {
    font-size: 24px;
    margin-top: 12px;
}

.purple h2 { color: #7565D9; }
.green h2 { color: #21A179; }
.orange h2 { color: #E49B42; }

/* Forms */

.form-section,
.charts-section,
.table-section {
    background: white;
    padding: 22px;
    border-radius: 13px;
    margin-bottom: 22px;
    box-shadow: 0 4px 15px rgba(30, 35, 65, 0.04);
}

.form-section h2,
.charts-section h2,
.table-section h2 {
    font-size: 17px;
    margin-bottom: 17px;
}

.expense-form {
    display: grid;
    grid-template-columns: 2fr 1fr 1.2fr auto;
    gap: 12px;
}

input,
select {
    width: 100%;
    min-width: 0;
    padding: 12px;
    border: 1px solid #E0E2EB;
    border-radius: 7px;
    font-size: 13px;
    outline: none;
    background: white;
}

input:focus,
select:focus {
    border-color: #7565D9;
}

button {
    padding: 12px 18px;
    background: #7565D9;
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
}

button:hover {
    opacity: 0.85;
    transform: translateY(-1px);
}

.budget-form {
    display: flex;
    gap: 12px;
}

.budget-form input {
    max-width: 350px;
}

/* Charts */

.chart-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.chart-box {
    min-width: 0;
    padding: 17px;
    border: 1px solid #ECECF3;
    border-radius: 10px;
}

.chart-box h3 {
    font-size: 14px;
    margin-bottom: 15px;
}

.chart-box canvas {
    width: 100% !important;
    height: 280px !important;
}

/* Table */

.table-wrapper {
    width: 100%;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
}

th {
    background: #F0EFF7;
    color: #555B75;
    font-size: 12px;
    text-align: left;
    padding: 13px;
}

td {
    padding: 13px;
    border-bottom: 1px solid #ECECF3;
    font-size: 13px;
}

.delete-btn {
    background: #E45B68;
    padding: 8px 12px;
    font-size: 11px;
}

.empty {
    color: #858BA3;
    padding: 15px 0;
}

footer {
    text-align: center;
    color: #858BA3;
    font-size: 12px;
    padding: 20px;
}

/* Mobile responsive design */

@media (max-width: 900px) {
    .sidebar {
        width: 175px;
    }

    .main-content {
        margin-left: 175px;
        padding: 20px;
    }

    .expense-form {
        grid-template-columns: 1fr 1fr;
    }

    .cards {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        padding: 15px;
    }

    .sidebar h2 {
        font-size: 18px;
        display: inline-block;
        margin: 0;
    }

    .side-label,
    .side-footer {
        display: none;
    }

    .sidebar a {
        display: inline-block;
        font-size: 12px;
        padding: 9px;
        margin: 5px 2px;
    }

    .main-content {
        margin-left: 0;
        padding: 15px;
    }

    header {
        align-items: flex-start;
        flex-direction: column;
        gap: 10px;
    }

    header h1 {
        font-size: 23px;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .expense-form {
        grid-template-columns: 1fr;
    }

    .budget-form {
        flex-direction: column;
    }

    .budget-form input {
        max-width: 100%;
    }

    .chart-grid {
        grid-template-columns: 1fr;
    }

    .chart-box canvas {
        height: 250px !important;
    }
}
