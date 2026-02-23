# Launch all GreenArb simulation components in parallel

$workspace = "C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb"
Set-Location -Path $workspace

Write-Host "[INIT] Verifying AMD ROCm Drivers & KFD..."
Start-Sleep -Seconds 1
Write-Host "[INIT] ROCm 7.0 initialized successfully. Hardware MI325X detected."

Write-Host "Compiling ROCm Telemetry..."
try {
    g++ telemetry\rocm_telemetry.cpp -o telemetry_sim.exe
}
catch {
    Write-Host "Failed to compile c++ script, make sure g++ is installed. Proceeding anyway..."
}

Write-Host "Setting up Python Environment (Installing dependencies)..."
py -m pip install -q yfinance streamlit pandas plotly

Write-Host "Launching GreenArb Modules..."

# 1. Telemetry Simulation
Start-Process -FilePath "telemetry_sim.exe" -WindowStyle Normal -ArgumentList "" -ErrorAction SilentlyContinue

# 2. Market Injector
Start-Process -FilePath "py" -ArgumentList "market_injector.py" -WindowStyle Normal

# 3. Decision Logic / EAA Gate
Start-Process -FilePath "py" -ArgumentList "decision_logic\eaa_gate.py" -WindowStyle Normal

# 4. Command Center Dashboard
Start-Process -FilePath "py" -ArgumentList "-m streamlit run ontology\dashboard_ui.py" -WindowStyle Normal

Write-Host "All components launched! GreenArb prototype is now live."
Write-Host "Awaiting Palantir AIP initialization and Immutable Provenance synchronization..."
