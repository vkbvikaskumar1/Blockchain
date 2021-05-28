# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 18:46:30 2020

@author: Vikas Kumar
"""

// Vikoins ICO

// Version of compiler
pragma solidity ^0.5.0;

contract Vikoin_ico {

    // Introducing the maximum number of Vikoins for sale
    uint public max_vikoins = 1000000;

    // Introducing the USD to Vikoins converstion rate
    uint public usd_to_vikoins = 1000;

    // Introducing the total number of Vikoins that have been bought by investors
    uint public total_vikoins_bought = 0;

    // Mapping from the investor address to its equity in Vikoins to USD
    mapping(address => uint) equity_vikoins;
    mapping(address => uint) equity_usd;

    // Checking if an investor can buy vikoins
    modifier can_buy_vikoins(uint usd_invested) {
        require (usd_invested * usd_to_vikoins + total_vikoins_bought <= max_vikoins);
        _;
    }

    // Getting the equity in Vikoins of an investor
    function equity_in_vikoins(address investor) external view returns (uint) {
        return equity_vikoins[investor];
    }

    // Getting the equity in USD of an investor
    function equity_in_usd(address investor) external view returns (uint) {
        return equity_usd[investor];
    }

    // Buying Vikoins
    function buy_vikoins(address investor, uint usd_invested) external
    can_buy_vikoins(usd_invested) {
        uint vikoins_bought = usd_invested * usd_to_vikoins;
        equity_vikoins[investor] += vikoins_bought;
        equity_usd[investor] = equity_vikoins[investor] / 1000;
        total_vikoins_bought += vikoins_bought;
    }

    // Selling Vikoins
    function sell_vikoins(address investor, uint vikoins_sold) external {
        equity_vikoins[investor] -= vikoins_sold;
        equity_usd[investor] = equity_vikoins[investor] / 1000;
        total_vikoins_bought -= vikoins_sold;
    }
}