function single_point_login(redirect,url,csrf_token,username,password){
    
    fetch(url,{
        method:"POST",
        headers: {
            'Accept':"application/json",
            'Content-Type':"application/json",
            'X-CSRFTOKEN':csrf_token,
        },
        body: JSON.stringify({
            "username": username,
            "password": password, 
        })
    }).then((res) =>{
            return res.json()
            }).then((res)=>{
            if(res["message"]==="DoesnotMatch"){
                alert("you inserted wrong password");
            }else if(res["message"]==="Fail"){
                alert("Something wents wrong");
            }else if(res["message"] ==="Success"){
                alert("Password change successfully");
                window.location.replace(redirect);
            }
        }).catch((fail) =>{
            alert(fail);
        })
};  

