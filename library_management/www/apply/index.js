$('#feedback-form').submit(e=>{
    e.preventDefault();
    console.log(e.target);
    makecall();
    
})

let makecall = async()=>{
    let formdata = $('#feedback-form').serializeArray().reduce(
        (obj,item)=>(obj[item.name]=item.value ,obj),{}
    );
    let imagedata = $('#image')[0].files[0];
    let imagefile = new FormData();
    if(imagedata){
        imagefile.append('file',imagedata)
    }
    if(formdata){
        let res = await $.ajax({
            url: '/api/resource/Feedback',
            type: 'POST',
            headers: {
                'Content-Type':'application/json',
                'X-Frappe-CSRF-Token': frappe.csrf_token
            },
            data: JSON.stringify(formdata),
            success: function(data){
                return data
            },
            error: function(data){
                return data
            }
        })
        console.log(res);
        if(res.data && imagedata){
            let images = await fetch('/api/method/upload_file',{
                headers:{
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                },
                method:'POST',
                body: imagefile
            })
            .then(res=>res.json())
            .then(data=>{
                console.log(data);
                if(data.message){
                    $.ajax({
                        url:`/api/resource/Feedback/${res.data.name}`,
                        type:'PUT',
                        headers:{
                            'Content-Type':'application/json',
                            'X-Frappe-CSRF-Token': frappe.csrf_token
                        },
                        data: JSON.stringify({image:data.message.file_url}),
                        success: function(data){
                            return data
                        },
                        error: function(data){
                            return data
                        }
                    })
                }
                
            })
        }
    }
}







// let imagefile = new FormData();
// imagefile.append('file_url',
//     'https://camo.githubusercontent.com/ae2d1da2d41cb35e3b3f4f450bc157d3b826f2bfd2f1a2b9c4e2845f28e2fd17/68747470733a2f2f692e626c6f67732e65732f3534356366382f6573362d6c6f676f2f6f726967696e616c2e706e67');

// //Append Attechment
// imagefile.append('doctype','Student')
// imagefile.append('docname','STU-00001')
// fetch('/api/method/upload_file',{
//     headers:{
//         'X-Frappe-CSRF-Token':frappe.csrf_token
//     },
//     method:'POST',
//     body:imagefile
// })
// .then(res=>res.json()  )