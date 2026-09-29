from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


# =========================================================
# ATM / BANKING DATA
# =========================================================

correct_pass = "admin123"

balance = 10000.00

attempts = 0

MAX_ATTEMPTS = 3

account_locked = False

transactions = []


# =========================================================
# HTML + CSS + JAVASCRIPT
# EVERYTHING IS IN THIS ONE FILE
# =========================================================

HTML = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>NovaBank ATM</title>


<style>

/* ======================================================
   RESET
====================================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


body {

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;

    min-height: 100vh;

    background:
        #070b14;

    color: #ffffff;

}


/* ======================================================
   SCROLLBAR
====================================================== */

::-webkit-scrollbar {

    width: 7px;

}


::-webkit-scrollbar-track {

    background: #0b1120;

}


::-webkit-scrollbar-thumb {

    background: #26344d;

    border-radius: 10px;

}


/* ======================================================
   LOGIN SCREEN
====================================================== */

.login-page {

    min-height: 100vh;

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 25px;

    position: relative;

    overflow: hidden;

    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(37, 99, 235, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(124, 58, 237, 0.20),
            transparent 30%
        ),
        #070b14;
}


.login-decoration {

    position: absolute;

    border-radius: 50%;

    filter: blur(1px);

    pointer-events: none;
}


.decoration-one {

    width: 350px;

    height: 350px;

    background:
        rgba(37, 99, 235, 0.08);

    top: -150px;

    left: -100px;
}


.decoration-two {

    width: 400px;

    height: 400px;

    background:
        rgba(124, 58, 237, 0.08);

    right: -150px;

    bottom: -170px;
}


.login-container {

    width: 100%;

    max-width: 440px;

    position: relative;

    z-index: 2;
}


.login-brand {

    text-align: center;

    margin-bottom: 28px;
}


.brand-logo {

    width: 72px;

    height: 72px;

    margin: 0 auto 18px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    font-size: 34px;

    box-shadow:
        0 15px 40px
        rgba(37, 99, 235, 0.28);
}


.login-brand h1 {

    font-size: 32px;

    font-weight: 800;

    letter-spacing: -1px;

    margin-bottom: 8px;
}


.login-brand p {

    color: #7d8ba3;

    font-size: 14px;
}


.login-card {

    background:
        rgba(15, 23, 42, 0.82);

    border:
        1px solid
        rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 32px;

    box-shadow:
        0 30px 80px
        rgba(0,0,0,0.4);

    backdrop-filter: blur(20px);
}


.input-label {

    display: block;

    color: #cbd5e1;

    font-size: 13px;

    font-weight: 600;

    margin-bottom: 9px;
}


.password-box {

    position: relative;

    margin-bottom: 18px;
}


.password-input {

    width: 100%;

    height: 52px;

    padding: 0 48px 0 16px;

    border-radius: 12px;

    border:
        1px solid
        #26344d;

    background:
        #0a1020;

    color: #ffffff;

    font-size: 15px;

    outline: none;

    transition: 0.2s;
}


.password-input::placeholder {

    color: #4d5c73;
}


.password-input:focus {

    border-color: #3b82f6;

    box-shadow:
        0 0 0 3px
        rgba(59,130,246,0.10);
}


.password-toggle {

    position: absolute;

    right: 14px;

    top: 50%;

    transform: translateY(-50%);

    background: none;

    border: none;

    color: #718096;

    cursor: pointer;

    font-size: 17px;
}


.login-button {

    width: 100%;

    height: 52px;

    border: none;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

    color: white;

    font-size: 15px;

    font-weight: 700;

    cursor: pointer;

    transition: 0.25s;

    box-shadow:
        0 12px 25px
        rgba(37,99,235,0.20);
}


.login-button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 18px 35px
        rgba(37,99,235,0.30);
}


.login-attempts {

    text-align: center;

    color: #596980;

    font-size: 12px;

    margin-top: 17px;
}


.login-footer {

    text-align: center;

    color: #4b5a70;

    font-size: 11px;

    margin-top: 20px;
}


/* ======================================================
   MESSAGES
====================================================== */

.alert {

    padding: 13px 15px;

    border-radius: 11px;

    margin-bottom: 18px;

    text-align: center;

    font-size: 13px;

    font-weight: 600;
}


.alert-success {

    color: #4ade80;

    background:
        rgba(34,197,94,0.08);

    border:
        1px solid
        rgba(34,197,94,0.18);
}


.alert-error {

    color: #fb7185;

    background:
        rgba(244,63,94,0.08);

    border:
        1px solid
        rgba(244,63,94,0.18);
}


/* ======================================================
   DASHBOARD
====================================================== */

.dashboard {

    min-height: 100vh;

    display: flex;

    background:
        #070b14;
}


/* ======================================================
   SIDEBAR
====================================================== */

.sidebar {

    width: 245px;

    min-height: 100vh;

    position: fixed;

    left: 0;

    top: 0;

    bottom: 0;

    background:
        #0a1020;

    border-right:
        1px solid
        rgba(255,255,255,0.06);

    padding: 25px 18px;

    display: flex;

    flex-direction: column;

    z-index: 10;
}


.sidebar-brand {

    display: flex;

    align-items: center;

    gap: 11px;

    padding: 4px 8px;

    margin-bottom: 42px;
}


.sidebar-logo {

    width: 40px;

    height: 40px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 11px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    font-size: 20px;
}


.sidebar-brand-text {

    font-weight: 800;

    font-size: 16px;
}


.sidebar-brand-text span {

    display: block;

    color: #52627a;

    font-size: 9px;

    font-weight: 500;

    letter-spacing: 1px;

    margin-top: 2px;
}


.menu-label {

    color: #45536a;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: 1.5px;

    padding-left: 11px;

    margin-bottom: 10px;
}


.menu-item {

    width: 100%;

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 12px 11px;

    margin-bottom: 5px;

    border: none;

    border-radius: 10px;

    background: transparent;

    color: #75849a;

    font-size: 13px;

    font-weight: 500;

    cursor: pointer;

    text-align: left;

    transition: 0.2s;
}


.menu-item:hover {

    color: #ffffff;

    background:
        rgba(59,130,246,0.08);
}


.menu-item.active {

    color: #ffffff;

    background:
        rgba(59,130,246,0.12);

    border:
        1px solid
        rgba(59,130,246,0.12);
}


.menu-icon {

    width: 24px;

    text-align: center;

    font-size: 16px;
}


.sidebar-bottom {

    margin-top: auto;
}


.secure-card {

    padding: 14px;

    border-radius: 12px;

    background:
        rgba(34,197,94,0.05);

    border:
        1px solid
        rgba(34,197,94,0.12);

    margin-bottom: 12px;
}


.secure-title {

    color: #52627a;

    font-size: 10px;

    margin-bottom: 5px;
}


.secure-status {

    color: #4ade80;

    font-size: 12px;

    font-weight: 600;
}


.logout-button {

    width: 100%;

    padding: 12px;

    border-radius: 10px;

    border:
        1px solid
        rgba(244,63,94,0.15);

    background:
        rgba(244,63,94,0.05);

    color: #fb7185;

    font-size: 13px;

    font-weight: 600;

    cursor: pointer;

    transition: 0.2s;
}


.logout-button:hover {

    background:
        rgba(244,63,94,0.12);
}


/* ======================================================
   MAIN
====================================================== */

.main {

    width: calc(100% - 245px);

    margin-left: 245px;

    padding: 30px 38px 50px;
}


.main-inner {

    max-width: 1250px;

    margin: auto;
}


/* ======================================================
   TOP BAR
====================================================== */

.topbar {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 28px;
}


.greeting h1 {

    font-size: 25px;

    font-weight: 700;

    letter-spacing: -0.5px;
}


.greeting p {

    color: #617087;

    font-size: 12px;

    margin-top: 5px;
}


.profile {

    display: flex;

    align-items: center;

    gap: 10px;

    padding: 6px 11px 6px 6px;

    border-radius: 30px;

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid
        rgba(255,255,255,0.06);
}


.profile-avatar {

    width: 32px;

    height: 32px;

    display: flex;

    justify-content: center;

    align-items: center;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    font-size: 14px;
}


.profile-name {

    color: #cbd5e1;

    font-size: 12px;

    font-weight: 600;
}


/* ======================================================
   BALANCE + ACCOUNT
====================================================== */

.overview-grid {

    display: grid;

    grid-template-columns:
        1.5fr 1fr;

    gap: 18px;

    margin-bottom: 25px;
}


.balance-card {

    min-height: 220px;

    padding: 28px;

    border-radius: 20px;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #1d4ed8,
            #4338ca 55%,
            #6d28d9
        );

    box-shadow:
        0 25px 50px
        rgba(37,99,235,0.16);
}


.balance-card::before {

    content: "";

    position: absolute;

    width: 280px;

    height: 280px;

    border-radius: 50%;

    right: -110px;

    top: -150px;

    background:
        rgba(255,255,255,0.08);
}


.balance-card::after {

    content: "";

    position: absolute;

    width: 180px;

    height: 180px;

    border-radius: 50%;

    right: 60px;

    bottom: -140px;

    background:
        rgba(255,255,255,0.05);
}


.balance-label {

    color: #c7d2fe;

    font-size: 11px;

    letter-spacing: 1px;

    position: relative;

    z-index: 2;
}


.balance-value {

    font-size: 43px;

    font-weight: 800;

    letter-spacing: -1.5px;

    margin-top: 9px;

    position: relative;

    z-index: 2;
}


.balance-change {

    margin-top: 8px;

    color: #c7d2fe;

    font-size: 11px;

    position: relative;

    z-index: 2;
}


.balance-bottom {

    position: absolute;

    bottom: 25px;

    left: 28px;

    right: 28px;

    display: flex;

    justify-content: space-between;

    align-items: center;

    z-index: 2;
}


.account-number {

    color: #c7d2fe;

    font-size: 11px;
}


.active-pill {

    padding: 6px 10px;

    border-radius: 20px;

    background:
        rgba(255,255,255,0.12);

    color: white;

    font-size: 10px;
}


/* ======================================================
   ACCOUNT CARD
====================================================== */

.account-card {

    min-height: 220px;

    border-radius: 20px;

    background:
        #0c1425;

    border:
        1px solid
        rgba(255,255,255,0.06);

    padding: 25px;
}


.card-title {

    font-size: 14px;

    font-weight: 700;

    margin-bottom: 20px;
}


.account-row {

    display: flex;

    justify-content: space-between;

    padding: 12px 0;

    border-bottom:
        1px solid
        rgba(255,255,255,0.05);
}


.account-row:last-child {

    border-bottom: none;
}


.account-row span:first-child {

    color: #596980;

    font-size: 11px;
}


.account-row span:last-child {

    color: #cbd5e1;

    font-size: 11px;

    font-weight: 600;
}


/* ======================================================
   QUICK ACTIONS
====================================================== */

.section-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 13px;
}


.section-header h2 {

    font-size: 15px;
}


.section-header span {

    color: #52627a;

    font-size: 11px;
}


.actions {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;

    margin-bottom: 25px;
}


.action-card {

    width: 100%;

    text-align: left;

    padding: 21px;

    border-radius: 16px;

    background:
        #0c1425;

    border:
        1px solid
        rgba(255,255,255,0.06);

    color: white;

    cursor: pointer;

    transition:
        transform 0.2s,
        border-color 0.2s,
        background 0.2s;
}


.action-card:hover {

    transform: translateY(-3px);

    background:
        #101a2e;

    border-color:
        rgba(59,130,246,0.35);
}


.action-icon {

    width: 43px;

    height: 43px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 12px;

    background:
        rgba(59,130,246,0.10);

    font-size: 20px;

    margin-bottom: 14px;
}


.action-card h3 {

    font-size: 13px;

    margin-bottom: 5px;
}


.action-card p {

    color: #596980;

    font-size: 10px;

    line-height: 1.5;
}


/* ======================================================
   BOTTOM GRID
====================================================== */

.bottom-grid {

    display: grid;

    grid-template-columns:
        1.5fr 1fr;

    gap: 18px;
}


/* ======================================================
   TRANSACTIONS
====================================================== */

.transactions-card {

    background:
        #0c1425;

    border:
        1px solid
        rgba(255,255,255,0.06);

    border-radius: 18px;

    padding: 23px;
}


.transaction-item {

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 13px 0;

    border-bottom:
        1px solid
        rgba(255,255,255,0.05);
}


.transaction-item:last-child {

    border-bottom: none;
}


.transaction-left {

    display: flex;

    align-items: center;

    gap: 11px;
}


.transaction-icon {

    width: 37px;

    height: 37px;

    display: flex;

    justify-content: center;

    align-items: center;

    border-radius: 10px;

    font-size: 16px;
}


.deposit-icon {

    background:
        rgba(34,197,94,0.08);
}


.withdraw-icon {

    background:
        rgba(239,68,68,0.08);
}


.transaction-name {

    font-size: 12px;

    font-weight: 600;

    color: #cbd5e1;
}


.transaction-date {

    color: #53627a;

    font-size: 9px;

    margin-top: 3px;
}


.transaction-amount {

    font-size: 12px;

    font-weight: 700;
}


.amount-positive {

    color: #4ade80;
}


.amount-negative {

    color: #fb7185;
}


.empty-transactions {

    text-align: center;

    padding: 30px;

    color: #4f5e75;

    font-size: 12px;
}


/* ======================================================
   SECURITY CARD
====================================================== */

.security-panel {

    background:
        #0c1425;

    border:
        1px solid
        rgba(255,255,255,0.06);

    border-radius: 18px;

    padding: 23px;
}


.security-status {

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 14px;

    border-radius: 12px;

    background:
        rgba(34,197,94,0.05);

    border:
        1px solid
        rgba(34,197,94,0.10);

    margin-bottom: 15px;
}


.security-circle {

    width: 35px;

    height: 35px;

    display: flex;

    justify-content: center;

    align-items: center;

    border-radius: 50%;

    background:
        rgba(34,197,94,0.10);
}


.security-status strong {

    display: block;

    font-size: 12px;

    color: #4ade80;

    margin-bottom: 3px;
}


.security-status span {

    color: #52627a;

    font-size: 9px;
}


.security-line {

    display: flex;

    justify-content: space-between;

    padding: 11px 0;

    border-bottom:
        1px solid
        rgba(255,255,255,0.05);
}


.security-line:last-child {

    border-bottom: none;
}


.security-line span:first-child {

    color: #52627a;

    font-size: 10px;
}


.security-line span:last-child {

    color: #cbd5e1;

    font-size: 10px;

    font-weight: 600;
}


/* ======================================================
   MODAL
====================================================== */

.modal {

    display: none;

    position: fixed;

    inset: 0;

    background:
        rgba(0,0,0,0.72);

    backdrop-filter:
        blur(7px);

    align-items: center;

    justify-content: center;

    padding: 20px;

    z-index: 100;
}


.modal-card {

    width: 100%;

    max-width: 390px;

    background:
        #0c1425;

    border:
        1px solid
        #26344d;

    border-radius: 20px;

    padding: 26px;

    box-shadow:
        0 30px 80px
        rgba(0,0,0,0.55);

    animation:
        modalIn 0.2s ease;
}


@keyframes modalIn {

    from {

        opacity: 0;

        transform:
            translateY(15px)
            scale(0.97);

    }

    to {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }

}


.modal-top {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 22px;
}


.modal-top h2 {

    font-size: 19px;
}


.modal-close {

    width: 32px;

    height: 32px;

    border: none;

    border-radius: 8px;

    background:
        rgba(255,255,255,0.05);

    color: #8a98ad;

    cursor: pointer;

    font-size: 18px;
}


.amount-label {

    color: #77869c;

    font-size: 11px;

    margin-bottom: 8px;

    display: block;
}


.amount-input {

    width: 100%;

    height: 55px;

    border-radius: 12px;

    border:
        1px solid
        #26344d;

    background:
        #070b14;

    color: white;

    font-size: 20px;

    padding: 0 16px;

    outline: none;

    margin-bottom: 15px;
}


.amount-input:focus {

    border-color: #3b82f6;
}


.confirm-button {

    width: 100%;

    height: 50px;

    border: none;

    border-radius: 11px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

    color: white;

    font-weight: 700;

    cursor: pointer;
}


/* ======================================================
   LOCKED
====================================================== */

.locked-page {

    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 25px;

    background:
        radial-gradient(
            circle at center,
            rgba(239,68,68,0.07),
            transparent 35%
        ),
        #070b14;
}


.locked-card {

    width: 100%;

    max-width: 450px;

    padding: 40px;

    border-radius: 24px;

    text-align: center;

    background:
        #0c1425;

    border:
        1px solid
        rgba(239,68,68,0.15);
}


.locked-icon {

    width: 85px;

    height: 85px;

    display: flex;

    align-items: center;

    justify-content: center;

    margin: 0 auto 20px;

    border-radius: 50%;

    background:
        rgba(239,68,68,0.08);

    font-size: 40px;
}


.locked-card h1 {

    color: #fb7185;

    font-size: 28px;

    margin-bottom: 10px;
}


.locked-card p {

    color: #64748b;

    font-size: 13px;

    line-height: 1.6;
}


/* ======================================================
   RESPONSIVE
====================================================== */

@media(max-width: 1000px) {

    .overview-grid {

        grid-template-columns: 1fr;

    }


    .bottom-grid {

        grid-template-columns: 1fr;

    }

}


@media(max-width: 800px) {

    .sidebar {

        width: 75px;

        padding: 20px 10px;

    }


    .sidebar-brand-text,

    .menu-label,

    .menu-item span:not(.menu-icon),

    .secure-card,

    .logout-button {

        display: none;

    }


    .sidebar-brand {

        justify-content: center;

    }


    .menu-item {

        justify-content: center;

    }


    .main {

        width: calc(100% - 75px);

        margin-left: 75px;

        padding: 25px 20px;

    }


    .actions {

        grid-template-columns:
            repeat(2, 1fr);

    }

}


@media(max-width: 600px) {

    .main {

        width: 100%;

        margin-left: 0;

        padding: 20px 15px 35px;

    }


    .sidebar {

        display: none;

    }


    .topbar {

        margin-bottom: 20px;

    }


    .greeting h1 {

        font-size: 21px;

    }


    .profile {

        display: none;

    }


    .balance-value {

        font-size: 34px;

    }


    .actions {

        grid-template-columns: 1fr;

    }


    .overview-grid {

        gap: 12px;

    }


    .balance-card,

    .account-card {

        min-height: 190px;

    }


    .login-card {

        padding: 25px 20px;

    }

}

</style>

</head>


<body>


{% if page == "login" %}


<!-- ====================================================
     LOGIN
===================================================== -->

<div class="login-page">


    <div class="login-decoration decoration-one"></div>

    <div class="login-decoration decoration-two"></div>


    <div class="login-container">


        <div class="login-brand">


            <div class="brand-logo">

                🏦

            </div>


            <h1>

                NovaBank

            </h1>


            <p>

                Secure digital banking

            </p>


        </div>


        <div class="login-card">


            {% if message %}

            <div class="alert {{ message_type }}">

                {{ message }}

            </div>

            {% endif %}


            <form
                method="POST"
                action="/login">


                <label class="input-label">

                    Enter your password

                </label>


                <div class="password-box">


                    <input
                        class="password-input"
                        id="password"
                        type="password"
                        name="password"
                        placeholder="Enter password"
                        required
                        autofocus>


                    <button
                        type="button"
                        class="password-toggle"
                        onclick="togglePassword()">

                        👁

                    </button>


                </div>


                <button
                    type="submit"
                    class="login-button">

                    Continue to Banking →

                </button>


            </form>


            <div class="login-attempts">

                Security attempts:
                <strong>
                    {{ attempts }}/3
                </strong>

            </div>


        </div>


        <div class="login-footer">

            🔒 Your banking session is protected

        </div>


    </div>

</div>


{% elif page == "dashboard" %}


<!-- ====================================================
     DASHBOARD
===================================================== -->

<div class="dashboard">


    <!-- SIDEBAR -->

    <aside class="sidebar">


        <div class="sidebar-brand">


            <div class="sidebar-logo">

                🏦

            </div>


            <div class="sidebar-brand-text">

                NovaBank

                <span>

                    DIGITAL BANKING

                </span>

            </div>


        </div>


        <div class="menu-label">

            Overview

        </div>


        <button
            class="menu-item active"
            onclick="goHome()">

            <span class="menu-icon">
                ⌂
            </span>

            <span>
                Dashboard
            </span>

        </button>


        <button
            class="menu-item"
            onclick="openModal('deposit')">

            <span class="menu-icon">
                ↓
            </span>

            <span>
                Deposit
            </span>

        </button>


        <button
            class="menu-item"
            onclick="openModal('withdraw')">

            <span class="menu-icon">
                ↑
            </span>

            <span>
                Withdraw
            </span>

        </button>


        <button
            class="menu-item"
            onclick="showTransactions()">

            <span class="menu-icon">
                ≡
            </span>

            <span>
                Transactions
            </span>

        </button>


        <div class="sidebar-bottom">


            <div class="secure-card">

                <div class="secure-title">

                    SECURITY

                </div>

                <div class="secure-status">

                    ● Protected

                </div>

            </div>


            <form
                method="POST"
                action="/logout">


                <button
                    type="submit"
                    class="logout-button">

                    🚪 Logout

                </button>


            </form>


        </div>


    </aside>


    <!-- MAIN -->

    <main class="main">


        <div class="main-inner">


            <!-- TOPBAR -->

            <div class="topbar">


                <div class="greeting">

                    <h1>
                        Good day, Account Holder 👋
                    </h1>

                    <p>
                        Here's your account overview
                    </p>

                </div>


                <div class="profile">

                    <div class="profile-avatar">
                        👤
                    </div>

                    <div class="profile-name">
                        Account Holder
                    </div>

                </div>


            </div>


            {% if message %}

            <div class="alert {{ message_type }}">

                {{ message }}

            </div>

            {% endif %}


            <!-- OVERVIEW -->

            <div class="overview-grid">


                <!-- BALANCE -->

                <div
                    class="balance-card"
                    id="balanceCard">


                    <div class="balance-label">

                        AVAILABLE BALANCE

                    </div>


                    <div class="balance-value">

                        ₹{{ "%.2f"|format(balance) }}

                    </div>


                    <div class="balance-change">

                        Available for transactions

                    </div>


                    <div class="balance-bottom">


                        <div class="account-number">

                            A/C •••• 2026

                        </div>


                        <div class="active-pill">

                            ● Active

                        </div>


                    </div>


                </div>


                <!-- ACCOUNT -->

                <div class="account-card">


                    <div class="card-title">

                        Account Details

                    </div>


                    <div class="account-row">

                        <span>
                            Account Type
                        </span>

                        <span>
                            Savings
                        </span>

                    </div>


                    <div class="account-row">

                        <span>
                            Account Number
                        </span>

                        <span>
                            **** 2026
                        </span>

                    </div>


                    <div class="account-row">

                        <span>
                            Currency
                        </span>

                        <span>
                            INR ₹
                        </span>

                    </div>


                    <div class="account-row">

                        <span>
                            Status
                        </span>

                        <span style="color:#4ade80;">
                            Active
                        </span>

                    </div>


                </div>


            </div>


            <!-- QUICK ACTIONS -->

            <div class="section-header">

                <h2>
                    Quick Actions
                </h2>

                <span>
                    Manage your money
                </span>

            </div>


            <div class="actions">


                <!-- BALANCE -->

                <form
                    method="POST"
                    action="/balance">


                    <button
                        class="action-card"
                        type="submit">


                        <div class="action-icon">

                            💰

                        </div>


                        <h3>

                            Check Balance

                        </h3>


                        <p>

                            View your current
                            account balance

                        </p>


                    </button>


                </form>


                <!-- DEPOSIT -->

                <button
                    class="action-card"
                    onclick="openModal('deposit')">


                    <div class="action-icon">

                        💵

                    </div>


                    <h3>

                        Deposit Money

                    </h3>


                    <p>

                        Add funds to your
                        bank account

                    </p>


                </button>


                <!-- WITHDRAW -->

                <button
                    class="action-card"
                    onclick="openModal('withdraw')">


                    <div class="action-icon">

                        💸

                    </div>


                    <h3>

                        Withdraw Money

                    </h3>


                    <p>

                        Withdraw funds
                        from your account

                    </p>


                </button>


            </div>


            <!-- BOTTOM -->

            <div class="bottom-grid">


                <!-- TRANSACTIONS -->

                <div
                    class="transactions-card"
                    id="transactions">


                    <div class="section-header">

                        <h2>
                            Recent Transactions
                        </h2>

                        <span>
                            Latest activity
                        </span>

                    </div>


                    {% if transactions %}


                        {% for transaction in transactions %}


                        <div class="transaction-item">


                            <div class="transaction-left">


                                <div
                                    class="transaction-icon
                                    {% if transaction.type == 'Deposit' %}
                                    deposit-icon
                                    {% else %}
                                    withdraw-icon
                                    {% endif %}">


                                    {% if transaction.type == 'Deposit' %}

                                        ↓

                                    {% else %}

                                        ↑

                                    {% endif %}


                                </div>


                                <div>


                                    <div class="transaction-name">

                                        {{ transaction.type }}

                                    </div>


                                    <div class="transaction-date">

                                        {{ transaction.date }}

                                    </div>


                                </div>


                            </div>


                            <div
                                class="
                                transaction-amount
                                {% if transaction.type == 'Deposit' %}
                                amount-positive
                                {% else %}
                                amount-negative
                                {% endif %}
                                ">


                                {% if transaction.type == 'Deposit' %}

                                    + ₹{{ "%.2f"|format(transaction.amount) }}

                                {% else %}

                                    - ₹{{ "%.2f"|format(transaction.amount) }}

                                {% endif %}


                            </div>


                        </div>


                        {% endfor %}


                    {% else %}


                        <div class="empty-transactions">

                            No transactions yet

                        </div>


                    {% endif %}


                </div>


                <!-- SECURITY -->

                <div class="security-panel">


                    <div class="section-header">

                        <h2>
                            Security
                        </h2>

                    </div>


                    <div class="security-status">


                        <div class="security-circle">

                            🔐

                        </div>


                        <div>

                            <strong>

                                Account Secure

                            </strong>

                            <span>

                                No security issues detected

                            </span>

                        </div>


                    </div>


                    <div class="security-line">

                        <span>
                            Login protection
                        </span>

                        <span>
                            Enabled
                        </span>

                    </div>


                    <div class="security-line">

                        <span>
                            Account status
                        </span>

                        <span style="color:#4ade80;">
                            Active
                        </span>

                    </div>


                    <div class="security-line">

                        <span>
                            Last access
                        </span>

                        <span>
                            Just now
                        </span>

                    </div>


                </div>


            </div>


        </div>


    </main>


</div>


<!-- ====================================================
     TRANSACTION MODAL
===================================================== -->

<div
    class="modal"
    id="transactionModal">


    <div class="modal-card">


        <div class="modal-top">


            <h2 id="modalTitle">

                Transaction

            </h2>


            <button
                class="modal-close"
                onclick="closeModal()">

                ×

            </button>


        </div>


        <form
            method="POST"
            id="transactionForm">


            <label class="amount-label">

                Enter Amount

            </label>


            <input
                class="amount-input"
                type="number"
                name="amount"
                min="1"
                step="0.01"
                placeholder="₹ 0.00"
                required
                autofocus>


            <button
                type="submit"
                class="confirm-button">

                Confirm Transaction

            </button>


        </form>


    </div>


</div>


{% elif page == "locked" %}


<!-- ====================================================
     LOCKED
===================================================== -->

<div class="locked-page">


    <div class="locked-card">


        <div class="locked-icon">

            🔒

        </div>


        <h1>

            Account Locked

        </h1>


        <p>

            Your account has been locked because
            the maximum number of incorrect login
            attempts has been reached.

        </p>


        <br>


        <div class="alert alert-error">

            3 failed login attempts

        </div>


        <p>

            Please contact the bank administrator
            to restore access.

        </p>


    </div>


</div>


{% endif %}


<script>


// =====================================================
// PASSWORD SHOW / HIDE
// =====================================================

function togglePassword() {

    const input =
        document.getElementById("password");


    if (!input) return;


    if (input.type === "password") {

        input.type = "text";

    }

    else {

        input.type = "password";

    }

}


// =====================================================
// TRANSACTION MODAL
// =====================================================

function openModal(type) {

    const modal =
        document.getElementById(
            "transactionModal"
        );


    const title =
        document.getElementById(
            "modalTitle"
        );


    const form =
        document.getElementById(
            "transactionForm"
        );


    if (!modal) return;


    modal.style.display = "flex";


    if (type === "deposit") {

        title.textContent =
            "💵 Deposit Money";


        form.action =
            "/deposit";

    }

    else {

        title.textContent =
            "💸 Withdraw Money";


        form.action =
            "/withdraw";

    }

}


function closeModal() {

    const modal =
        document.getElementById(
            "transactionModal"
        );


    if (modal) {

        modal.style.display = "none";

    }

}


// =====================================================
// CLICK OUTSIDE MODAL
// =====================================================

window.onclick = function(event) {

    const modal =
        document.getElementById(
            "transactionModal"
        );


    if (
        modal &&
        event.target === modal
    ) {

        closeModal();

    }

};


// =====================================================
// DASHBOARD
// =====================================================

function goHome() {

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


function showTransactions() {

    const section =
        document.getElementById(
            "transactions"
        );


    if (section) {

        section.scrollIntoView({
            behavior: "smooth"
        });

    }

}

</script>


</body>

</html>

"""


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if account_locked:

        return render_template_string(
            HTML,
            page="locked",
            message=None,
            message_type=None,
            attempts=attempts,
            balance=balance,
            transactions=transactions
        )


    return render_template_string(
        HTML,
        page="login",
        message=None,
        message_type=None,
        attempts=attempts,
        balance=balance,
        transactions=transactions
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    global attempts
    global account_locked


    password = request.form.get(
        "password",
        ""
    )


    attempts += 1


    # -----------------------------------------
    # CORRECT PASSWORD
    # -----------------------------------------

    if password == correct_pass:

        attempts = 0


        return render_template_string(
            HTML,
            page="dashboard",
            message="Login successful. Welcome back! ✓",
            message_type="alert-success",
            attempts=attempts,
            balance=balance,
            transactions=transactions
        )


    # -----------------------------------------
    # ACCOUNT LOCK
    # -----------------------------------------

    if attempts >= MAX_ATTEMPTS:

        account_locked = True


        return render_template_string(
            HTML,
            page="locked",
            message=None,
            message_type=None,
            attempts=attempts,
            balance=balance,
            transactions=transactions
        )


    remaining = MAX_ATTEMPTS - attempts


    return render_template_string(
        HTML,
        page="login",
        message=
            f"Incorrect password. "
            f"{remaining} attempt(s) remaining.",
        message_type="alert-error",
        attempts=attempts,
        balance=balance,
        transactions=transactions
    )


# =========================================================
# CHECK BALANCE
# =========================================================

@app.route("/balance", methods=["POST"])
def check_balance():

    return render_template_string(
        HTML,
        page="dashboard",
        message=
            f"Current available balance: "
            f"₹{balance:.2f}",
        message_type="alert-success",
        attempts=attempts,
        balance=balance,
        transactions=transactions
    )


# =========================================================
# DEPOSIT
# =========================================================

@app.route("/deposit", methods=["POST"])
def deposit():

    global balance


    try:

        amount = float(
            request.form.get(
                "amount",
                0
            )
        )

    except ValueError:

        amount = 0


    if amount <= 0:

        message = (
            "Please enter a valid amount."
        )

        message_type = "alert-error"


    else:

        balance += amount


        transactions.insert(
            0,
            {
                "type": "Deposit",
                "amount": amount,
                "date":
                    datetime.now().strftime(
                        "%d %b %Y, %I:%M %p"
                    )
            }
        )


        # Keep only latest 8 transactions

        if len(transactions) > 8:

            transactions.pop()


        message = (
            f"₹{amount:.2f} deposited successfully."
        )

        message_type = "alert-success"


    return render_template_string(
        HTML,
        page="dashboard",
        message=message,
        message_type=message_type,
        attempts=attempts,
        balance=balance,
        transactions=transactions
    )


# =========================================================
# WITHDRAW
# =========================================================

@app.route("/withdraw", methods=["POST"])
def withdraw():

    global balance


    try:

        amount = float(
            request.form.get(
                "amount",
                0
            )
        )

    except ValueError:

        amount = 0


    if amount <= 0:

        message = (
            "Please enter a valid amount."
        )

        message_type = "alert-error"


    elif amount > balance:

        message = (
            "Insufficient balance."
        )

        message_type = "alert-error"


    else:

        balance -= amount


        transactions.insert(
            0,
            {
                "type": "Withdraw",
                "amount": amount,
                "date":
                    datetime.now().strftime(
                        "%d %b %Y, %I:%M %p"
                    )
            }
        )


        if len(transactions) > 8:

            transactions.pop()


        message = (
            f"₹{amount:.2f} withdrawn successfully."
        )

        message_type = "alert-success"


    return render_template_string(
        HTML,
        page="dashboard",
        message=message,
        message_type=message_type,
        attempts=attempts,
        balance=balance,
        transactions=transactions
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout", methods=["POST"])
def logout():

    return redirect(
        url_for("home")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )