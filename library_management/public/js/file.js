frappe.pages['page'].on_page_load = function (wrapper) {
    console.log("Custom Page JS Loaded");

    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "Demo Page",
        single_column: true
    });

    page.main.html(`
        <div style="padding: 20px;">
            <h3>Hello from Page JS</h3>
            <p>This page is loaded using page_js hook.</p>
        </div>
    `);
};
