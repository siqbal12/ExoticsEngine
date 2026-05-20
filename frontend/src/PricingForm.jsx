import React, { useState } from 'react';

const initialState = {
  diffusionModelType: 'GBM',
  S0: 100,
  vol: 0.2,
  T: 1,
  r: 0.0375,
  V0: 0.04,
  kappa: 2,
  theta: 0.04,
  volvol: 0.5,
  corr: -0.5,
  lmbda: 0.5,
  jumpMean: 0,
  jumpVol: 0.2,
  optionType: 'Vanilla',
  barrierLevel: 100,
  barrierActivationType: 'In',
  barrierDirectionType: 'Up',
  K: 100,
  payoffType: 'Call',
  pricerType: 'Monte Carlo',
  numPaths: 10000,
  numSteps: 100,
  varianceReductionType: 'None',
  greekEstimatorType: 'Resimulation',
  greekType: 'Delta',
  controlVariable: 'S(T)',
};

export default function PricingForm() {
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('http://localhost:5001/api/price', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: 'Failed to fetch price' });
    }
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', height: '100vh' }}>
      <form
        onSubmit={handleSubmit}
        style={{
          width: 650,
          padding: 20,
          borderRight: '1px solid #ccc',
          display: 'flex',
          flexDirection: 'column',
          gap: 10,
        }}
      >
        <label>
          Diffusion Model:
          <select name="diffusionModelType" value={form.diffusionModelType} onChange={handleChange}>
            <option value="GBM">GBM</option>
            <option value="Heston">Heston</option>
            <option value="Jump Diffusion">Jump Diffusion</option>
            {/* Add more if needed */}
          </select>
        </label>

        {/*<h3>Common Parameters</h3>*/}

        {/* GBM and Heston Common Parameters - Side by Side */}
        <div style={{ display: 'flex', gap: 20 }}>
          {/* Left Column - Common Parameters */}
          <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 10 }}>
            <label>
              S0:
              <input type="number" name="S0" value={form.S0} onChange={handleChange} />
            </label>
            <label>
              vol:
              <input type="number" name="vol" value={form.vol} onChange={handleChange} />
            </label>
            <label>
              T:
              <input type="number" name="T" value={form.T} onChange={handleChange} />
            </label>
            <label>
              r:
              <input type="number" name="r" value={form.r} onChange={handleChange} />
            </label>
            <hr />
          </div>

          {form.diffusionModelType === 'Heston' && (
            <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 10 }}>
              <label>
                V0:
                <input type="number" name="V0" value={form.V0} onChange={handleChange} step="0.01" />
              </label>
              <label>
                Kappa:
                <input type="number" name="kappa" value={form.kappa} onChange={handleChange} step="0.1" />
              </label>
              <label>
                Theta:
                <input type="number" name="theta" value={form.theta} onChange={handleChange} step="0.01" />
              </label>
              <label>
                VolVol:
                <input type="number" name="volvol" value={form.volvol} onChange={handleChange} step="0.1" />
              </label>
              <label>
                Corr:
                <input type="number" name="corr" value={form.corr} onChange={handleChange} step="0.1" min="-1" max="1" />
              </label>
            </div>
          )}

          {form.diffusionModelType === 'Jump Diffusion' && (
            <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 10 }}>
              <label>
                Lambda:
                <input type="number" name="Lambda" value={form.lmbda} onChange={handleChange} step="0.01" />
              </label>
              <label>
                Jump Mean:
                <input type="number" name="Jump Mean" value={form.jumpMean} onChange={handleChange} step="0.01" />
              </label>
              <label>
                Jump Vol:
                <input type="number" name="Jump Vol" value={form.jumpVol} onChange={handleChange} step="0.01" />
              </label>
            </div>
          )}

        </div>

        <hr style={{ margin: '10px 0', border: 'none', borderTop: '1px solid #ccc' }} />

        <label>
          Option Type:
          <select name="optionType" value={form.optionType} onChange={handleChange}>
            <option value="Vanilla">Vanilla</option>
            <option value="Arithmetic Asian">Arithmetic Asian</option>
            <option value="Geometric Asian">Geometric Asian</option>
            <option value="Barrier">Barrier</option>
            <option value="Digital">Digital</option>
            {/* Add more if needed */}
          </select>
        </label>

        <label>
          Payoff Type:
          <select name="payoffType" value={form.payoffType} onChange={handleChange}>
            <option value="Call">Call</option>
            <option value="Put">Put</option>
          </select>
        </label>

        <label>
          K:
          <input type="number" name="K" value={form.K} onChange={handleChange} />
        </label>

        {
          form.optionType === 'Barrier' && (
            <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 10, margin: '0 auto' }}>
              <label>
                Barrier Level:
                <input
                  type="number"
                  name="barrierLevel"                   // <-- changed to match state key
                  value={form.barrierLevel}
                  onChange={handleChange}
                />
              </label>

              <label>
                Barrier Activation Type:
                <select
                  name="barrierActivationType"         // <-- changed to match state key
                  value={form.barrierActivationType}
                  onChange={handleChange}
                >
                  <option value="In">In</option>
                  <option value="Out">Out</option>
                </select>
              </label>

              <label>
                Barrier Direction Type:
                <select
                  name="barrierDirectionType"          // <-- changed to match state key
                  value={form.barrierDirectionType}
                  onChange={handleChange}
                >
                  <option value="Up">Up</option>
                  <option value="Down">Down</option>
                </select>
              </label>
            </div>
          )
        }


        <hr style={{ margin: '10px 0', border: 'none', borderTop: '1px solid #ccc' }} />
        <label>
          Pricer Type:
          <select name="pricerType" value={form.pricerType} onChange={handleChange}>
            <option value="Monte Carlo">Monte Carlo</option>
            {/* Add more if needed */}
          </select>
        </label>
        <label>
          Num Paths:
          <input type="number" name="numPaths" value={form.numPaths} onChange={handleChange} />
        </label>
        <label>
          Num Steps:
          <input type="number" name="numSteps" value={form.numSteps} onChange={handleChange} />
        </label>
        <label>
          Variance Reduction Method:
          <select name="varianceReductionType" value={form.varianceReductionType} onChange={handleChange}>
            <option value="None">None</option>
            <option value="Antithetic">Antithetic</option>
            <option value="Control">Control</option>
            <option value="Stratified Sampling">Stratified Sampling</option>
            {/* Add more if needed */}
          </select>
        </label>
        {form.varianceReductionType === 'Control' && (
              <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 10, margin: '0 auto' }}>

          <label>
            Control Variable:
            <select name="controlVariable" value={form.controlVariable} onChange={handleChange}>
              <option value="S(T)">S(T)</option>
              <option value="Vanilla Call">Vanilla Call</option>
              <option value="Vanilla Put">Vanilla Put</option>
              <option value="Geometric Asian Call">Geometric Asian Call</option>
              <option value="Geometric Asian Put">Geometric Asian Put</option>
              <option value="Digital Call">Digital Call</option>
              <option value="Digital Put">Digital Put</option>
              {/* Add more if needed */}
            </select>
          </label>
        </div>
      )}

        <hr style={{ margin: '10px 0', border: 'none', borderTop: '1px solid #ccc' }} />

        <label>
          Greek Estimator:
          <select name="greekEstimatorType" value={form.greekEstimatorType} onChange={handleChange}>
            <option value="Resimulation">Resimulation</option>
            <option value="Pathwise Differentiation">Pathwise Differentiation</option>
            {/* Add more if needed */}
          </select>
        </label>
        <label>
          Greek:
          <select name="greekType" value={form.greekType} onChange={handleChange}>
            <option value="Delta">Delta</option>
            <option value="Gamma">Gamma</option>
            <option value="Theta">Theta</option>
            <option value="Vega">Vega</option>
            <option value="Rho">Rho</option>
            {/* Add more if needed */}
          </select>
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Pricing...' : 'Price'}
        </button>
      </form>
<div style={{ padding: 40, flex: 1 }}>
  {result && (
    result.error ? (
      <div style={{ color: '#d32f2f', fontSize: '16px', fontWeight: 'bold' }}>
        Error: {result.error}
      </div>
    ) : (
      <div>
        <h1 style={{ marginBottom: 30, color: '#333' }}>Results</h1>

        {/* Price Section */}
        <div style={{
          backgroundColor: '#f5f5f5',
          padding: 20,
          borderRadius: 8,
          marginBottom: 20,
          borderLeft: '4px solid #1976d2'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#1976d2' }}>Price</h3>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#333', marginBottom: 10 }}>
            ${result['Estimated Price'].toFixed(2)}
          </div>
          <div style={{ fontSize: '14px', color: '#666' }}>
            SE: {result['Estimated Price Standard Error'].toFixed(5)}
          </div>
          <div style={{ fontSize: '14px', color: '#888', marginTop: 8 }}>
            95% CI: [${(result['Estimated Price'] - 1.96 * result['Estimated Price Standard Error']).toFixed(2)}, ${(result['Estimated Price'] + 1.96 * result['Estimated Price Standard Error']).toFixed(2)}]
          </div>
        </div>

        {/* Greek Section */}
        <div style={{
          backgroundColor: '#f5f5f5',
          padding: 20,
          borderRadius: 8,
          marginBottom: 20,
          borderLeft: '4px solid #388e3c'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#388e3c' }}>{form.greekType} (Approximate)</h3>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#333', marginBottom: 10 }}>
            {result['Estimated Greek'].toFixed(5)}
          </div>
          <div style={{ fontSize: '14px', color: '#666' }}>
            SE: {result['Estimated Greek (Approximate) Standard Error'].toFixed(5)}
          </div>
          <div style={{ fontSize: '14px', color: '#888', marginTop: 8 }}>
            95% CI: [{(result['Estimated Greek'] - 1.96 * result['Estimated Greek (Approximate) Standard Error']).toFixed(5)}, {(result['Estimated Greek'] + 1.96 * result['Estimated Greek (Approximate) Standard Error']).toFixed(5)}]
          </div>
        </div>

        {/* Runtime Section */}
        <div style={{
          backgroundColor: '#f5f5f5',
          padding: 20,
          borderRadius: 8,
          borderLeft: '4px solid #f57c00'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#f57c00' }}>Performance</h3>
          <div style={{ fontSize: '16px', color: '#333' }}>
            Runtime: <span style={{ fontWeight: 'bold' }}>{result['Runtime (s)'].toFixed(5)}s</span>
          </div>
        </div>
      </div>
    )
  )}
</div>

      {/*<div style={{ padding: 40, flex: 1 }}>*/}
      {/*  {result && (*/}
      {/*    result.error ? (*/}
      {/*      <div style={{ color: 'red' }}>Error: {result.error}</div>*/}
      {/*    ) : (*/}
      {/*      <div>*/}
      {/*        <h2>*/}
      {/*          Price: $ {result['Estimated Price'].toFixed(2)}*/}
      {/*        </h2>*/}
      {/*        <h3>*/}
      {/*          Price SE: {result['Estimated Price Standard Error'].toFixed(5)}*/}
      {/*        </h3>*/}
      {/*        <h3>*/}
      {/*          Price 95% CI: ($ {(result['Estimated Price'] - 1.96 * result['Estimated Price Standard Error']).toFixed(2)}, $ {(result['Estimated Price'] + 1.96 * result['Estimated Price Standard Error']).toFixed(2)})*/}
      {/*        </h3>*/}
      {/*        <h2>*/}
      {/*          Greek: {result['Estimated Greek'].toFixed(5)}*/}
      {/*        </h2>*/}
      {/*        <h3>*/}
      {/*          Greek (Approximate) SE: {result['Estimated Greek (Approximate) Standard Error'].toFixed(5)}*/}
      {/*        </h3>*/}
      {/*        <h3>*/}
      {/*          Greek (Approximate) 95% CI: (*/}
      {/*          {(result['Estimated Greek'] - 1.96 * result['Estimated Greek (Approximate) Standard Error']).toFixed(2)},*/}
      {/*          {(result['Estimated Greek'] + 1.96 * result['Estimated Greek (Approximate) Standard Error']).toFixed(2)}*/}
      {/*          )*/}
      {/*        </h3>*/}
      {/*        <h2>*/}
      {/*          Runtime: {result['Runtime (s)'].toFixed(5)} (s)*/}
      {/*        </h2>*/}


      {/*      </div>*/}
      {/*    )*/}
      {/*  )}*/}
      {/*</div>*/}

    </div>
  );
}
