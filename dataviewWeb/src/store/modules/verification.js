const verification = {
    state: {
        UserName: "",
        UserNo: "",
        AuthorityLevel: "",
        Token:"",
        Address: "ws://127.0.0.1:4200/",
        // Address: "ws://10.180.180.191:4200/",
    },
    mutations: {
        receiveInfo (state, payload){
            state.UserName = payload.UserName;
            state.UserNo = payload.UserNo;
            state.AuthorityLevel = payload.AuthorityLevel;
            state.Token = payload.Token;
            sessionStorage.setItem('verification', JSON.stringify(payload));
        },
        EventListener(state){
            let text = JSON.parse(sessionStorage.getItem('verification'));
           state.UserName = text.UserName;
            state.UserNo = text.UserNo;
            state.AuthorityLevel = text.AuthorityLevel;
            state.Token = text.Token;
        }
    }
};

export default verification;