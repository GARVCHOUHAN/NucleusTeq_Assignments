import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../project/common/input/Input";
import Button from "../project/common/button/Button";
import AuthService from "../../../services/auth-service";
import { useAuth } from "../../../hooks/use-auth";
import { ROUTES } from "../../../constants/routes";

function LoginForm(){

const navigate=useNavigate();
const {login}=useAuth();

const [email,setEmail]=useState("");
const [password,setPassword]=useState("");
const [loading,setLoading]=useState(false);
const [error,setError]=useState("");

async function handleLogin(e){
    e.preventDefault();
    setLoading(true);
    setError("");

    try{
    const response=await AuthService.login({email:email,password:password});
    login(response);
    navigate(ROUTES.DASHBOARD);
    }
    catch(err){

    const detail=err.response?.data?.detail;

    if(Array.isArray(detail)){
    setError(detail[0].msg);
    }
    else{
        setError(detail || "Login failed");}

    }
    finally{
    setLoading(false);
    }

}


return(
    <form onSubmit={handleLogin}>

    <Input
    label="Email"
    type="email"
    value={email}
    onChange={(e)=>setEmail(e.target.value)}
    />

    <Input
    label="Password"
    type="password"
    value={password}
    onChange={(e)=>setPassword(e.target.value)}
    />

    {error && <p>{error}</p>}

    <Button type="submit" disabled={loading}>
    {loading?"Logging In...":"Login"}
    </Button>

    </form>
);

}

export default LoginForm;