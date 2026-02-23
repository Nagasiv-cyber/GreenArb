"""
GreenArb - The Live "Profit Gate" (Palantir AIP Simulation)
Evaluates Synthetic/Real Alpha Signals against real-time Hardware & Environmental costs.
"""

import os
import json
import time
import csv
import random
from datetime import datetime

TELEMETRY_PIPE = r"C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb\telemetry_output.json"
MARKET_FEED_PIPE = r"C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb\market_feed.json"
LOG_OUTPUT = r"C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb\decision_logic\eaa_logs.csv"

os.makedirs(os.path.dirname(LOG_OUTPUT), exist_ok=True)

class EAAGateSimulator:
    def __init__(self):
        self.total_saved_watts = 0.0
        self._init_log_file()

    def _init_log_file(self):
        with open(LOG_OUTPUT, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "time_str", "gpu_power_w", "gpu_temp_c", "vram_bandwidth_gbs",
                "vram_efficiency_pct", "carbon_intensity", "net_spread_profit", 
                "total_cost", "action", "saved_watts", "green_alpha_score",
                "infy_nse", "infy_adr", "usd_inr", "carbon_credit_value", "carbon_tax", "final_profit"
            ])

    def poll_telemetry(self):
        try:
            if not os.path.exists(TELEMETRY_PIPE):
                return None
            with open(TELEMETRY_PIPE, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            return None

    def poll_market_feed(self):
        try:
            if not os.path.exists(MARKET_FEED_PIPE):
                return None
            with open(MARKET_FEED_PIPE, 'r') as f:
                data = json.load(f)
            return data.get("prices", {})
        except Exception as e:
            return None

    def calculate_electricity_surge(self):
        return random.uniform(2.0, 5.0)

    def trigger_os_throttle(self):
        print(">> OS_EVENT TRIGGERED: 'Throttle' command dispatched to AMD hardware.")
        return "THROTTLE_GPU"
        
    def trigger_burst_mode(self):
        print(">> OS_EVENT TRIGGERED: 'Burst Execution' routed to UL3524 Alveo FPGA in NY4.")
        return "EXECUTE_TRADE"

    def run_simulation_loop(self):
        print("Starting EAA Live Dual-Revenue Gate Simulation...")
        while True:
            telemetry = self.poll_telemetry()
            prices = self.poll_market_feed()
            
            if not telemetry or not prices:
                time.sleep(0.5)
                continue

            gpu_watts = telemetry.get("gpu_power_w", 0)
            gpu_temp = telemetry.get("gpu_temp_c", 0)
            vram_bw = telemetry.get("vram_bandwidth_gbs", 0)
            vram_eff = telemetry.get("vram_efficiency_pct", 0)
            carbon_intensity = telemetry.get("carbon_intensity_gCO2_kWh", 0)
            
            infy_nse = prices.get("INFY_NSE", 0)
            infy_adr = prices.get("INFY_ADR", 0)
            usd_inr = prices.get("USD_INR", 0)
            
            if infy_nse == 0 or usd_inr == 0:
                time.sleep(0.5)
                continue
                
            converted_adr_inr = infy_adr * usd_inr
            net_spread_profit = abs(converted_adr_inr - infy_nse)
            
            elec_surge = self.calculate_electricity_surge()
            grid_carbon_factor = carbon_intensity * 0.001
            total_cost = (gpu_watts * grid_carbon_factor) + elec_surge

            # FINAL PITCH: Simulated Peak Hours Penalty (18:00 to 21:00) 2026 pricing
            current_hour = datetime.now().hour
            if 18 <= current_hour <= 21:
                carbon_tax = carbon_intensity * 0.15
            else:
                carbon_tax = 0.0
                
            # Dual-Revenue Calculator
            saved_watts_potential = max(0, 500 - gpu_watts) # 500W TDP limit
            carbon_credit_value = saved_watts_potential * 0.05
            
            total_revenue = net_spread_profit + carbon_credit_value
            total_liabilities = total_cost + carbon_tax
            
            green_alpha_score = max(0, min(100, 100 - (carbon_intensity / 10.0)))
            
            action = "EXECUTE_TRADE"
            saved_watts = 0.0
            final_profit = 0.0
            
            if total_revenue <= total_liabilities:
                action = self.trigger_os_throttle()
                saved_watts = float(saved_watts_potential)
                self.total_saved_watts += saved_watts
                print(f"[REJECT_TRADE] Rev: ₹{total_revenue:.2f} < Liab: ₹{total_liabilities:.2f} | Tax: ₹{carbon_tax:.2f} | Watts Saved: {saved_watts:.1f} W")
            else:
                action = self.trigger_burst_mode()
                final_profit = total_revenue - total_liabilities
                print(f"[ACCEPT_TRADE] Rev: ₹{total_revenue:.2f} > Liab: ₹{total_liabilities:.2f} | Pure Alpha: ₹{final_profit:.2f} | Burst Microsec: 1.8μs")

            with open(LOG_OUTPUT, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    telemetry["timestamp"],
                    datetime.now().strftime("%H:%M:%S.%f")[:-3],
                    gpu_watts,
                    gpu_temp,
                    vram_bw,
                    vram_eff,
                    carbon_intensity,
                    net_spread_profit,
                    total_cost,
                    action,
                    saved_watts,
                    green_alpha_score,
                    infy_nse,
                    infy_adr,
                    usd_inr,
                    carbon_credit_value,
                    carbon_tax,
                    final_profit
                ])

            time.sleep(0.5)

if __name__ == "__main__":
    simulator = EAAGateSimulator()
    simulator.run_simulation_loop()
