// Copyright (c) 2025, Dakshit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Client Side Scripting", {
    // setup(frm) {
    //     console.log("Setup event");
    // },

    onload(frm) {
        console.log("Form Loaded");
    },

    // onload_post_render(frm) {
    //     console.log("After rendering UI");
    // },

    refresh(frm) {
        if(frm.is_new())
        {
            frm.set_intro('Now You Can Create a New Client Side Scripting')
        }
        else{
            frm.set_intro('Now You Can Edit Client Side Scripting')
        }
        console.log("Form Refreshed");
        frm.add_custom_button("Click Me", () => {
            frappe.msgprint("Hello!");
        });
    },

    validate:function(frm) {
        frm.set_value('full_name',frm.doc.first_name+" "+frm.doc.middle_name+" "+frm.doc.last_name)
        let row = frm.add_child('family_members',{
            name1:'Dakshit Gajipara',
            relation: 'Brother',
            age : 22,
        })
    },

    enable:function(frm){
        frm.set_df_property('first_name','reqd',1)
        frm.refresh_field('first_name')

        frm.set_df_property('middle_name','read only',1)
        frm.refresh_field('middle_name')

        frm.toggle_reqd('age',true)


    },


    // before_save(frm) {
    //     console.log("Before Save Executed");
    // },

    after_save(frm) {
        console.log("Saved Successfully");
    },

    // before_submit(frm) {
    //     console.log("Before Submit");
    // },

    on_submit(frm) {
        console.log("Submitted");
    },

    // before_cancel(frm) {
    //     console.log("Before Cancel");
    // },

    after_cancel(frm) {
        console.log("Cancelled");
    },

    // timeline_refresh(frm) {
    //     console.log("Timeline refresh");
    // },

    my_field(frm) {
        console.log("Field changed:", frm.doc.my_field);
    }

    

});

