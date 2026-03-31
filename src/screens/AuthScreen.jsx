import { useState } from 'react';
import { signInWithGoogle, signInWithEmail, signUpWithEmail } from '../lib/supabase';
import { Particles } from '../components/UI';

export default function AuthScreen() {
  const [mode, setMode] = useState('login'); // login | signup
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { error: authError } = mode === 'login'
        ? await signInWithEmail(email, password)
        : await signUpWithEmail(email, password);

      if (authError) setError(authError.message);
    } catch (err) {
      setError('Something went wrong');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="screen-center">
      <Particles type="dust" count={15} />
      <div className="auth-container fade-in">
        <div className="auth-icon">🕯️</div>
        <h1 className="auth-title">Quest</h1>
        <p className="auth-subtitle">Your daily dungeon awaits</p>

        <button className="btn-google" onClick={signInWithGoogle}>
          Continue with Google
        </button>

        <div className="auth-divider">
          <span>or</span>
        </div>

        <div className="auth-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="input-field"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="input-field"
          />
          {error && <div className="auth-error">{error}</div>}
          <button
            className="btn-primary"
            onClick={handleSubmit}
            disabled={loading || !email || !password}
          >
            {loading ? '...' : mode === 'login' ? 'Enter' : 'Create Account'}
          </button>
        </div>

        <button
          className="auth-toggle"
          onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
        >
          {mode === 'login' ? "Don't have an account? Sign up" : 'Already have an account? Log in'}
        </button>
      </div>
    </div>
  );
}
