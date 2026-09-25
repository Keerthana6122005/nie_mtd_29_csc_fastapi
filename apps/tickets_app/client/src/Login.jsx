import { useState } from 'react';
import api from './api';


function Login() {
    const [form, setForm] = useState({username:'', password:''});
    const onLogin = async () => {
        const data = new URLSearchParams();
        data.append('username', form.username);
        data.append('password', form.password);
        try {
            const response = await api.post('/login', data);
            if(response.status !== 200) {
                alert(response.data.detail);
                return;
            }
            alert('Logged In');
           alert (response.data.access_token);
        } catch(error) {
            alert(error.response?.data?.detail || 'Login failed');
        }
    };
   
    return (
    
         <div className="container mt-4">
            <div className="card p-4 mx-auto" style={{maxWidth: '500px'}}>
                <h2>Login</h2>
                <label className="form-label">
                    Username
                </label>
                <input
                    className="form-control mb-3"
                    value={form.username}
                    onChange={ e => setForm( {...form, username:e.target.value} ) }
                />
                <label className="form-label">Password</label>

                <input
                    type="password"
                    className="form-control mb-3"
                    value={form.password}
                    onChange={ e => setForm( {...form, password:e.target.value} ) }
                />


              

                <button className="btn btn-primary" onClick={onLogin}>Login</button>
            </div>
        </div>
        
    );
}

export default Login;