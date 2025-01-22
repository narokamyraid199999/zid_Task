frappe.provide('rukn_ecommerce');



frappe.pages['zid-import-product'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'ZID Import Product',
		single_column: true
	});

	new rukn_ecommerce.ProductImporter(wrapper);
}


rukn_ecommerce.ProductImporter = class {

	constructor(wrapper) {

		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;
		this.init();
		this.syncRunning = false;
	}

	init() {
		frappe.run_serially([
			() => this.addMarkup(),
			() => this.fetchProductCount(),
			() => this.addTable(),
			() => this.listen(),
		]);
	}

	addMarkup() {

		const _markup = $(`
            <div class="row">
                <div class="col-lg-8 d-flex align-items-stretch">
                    <div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                        <h5 class="border-bottom pb-2">Products in Salla</h5>
                        <div id="salla-product-list">
                            <div class="text-center">Loading...</div>
                        </div>
                        <div class="salla-datatable-footer mt-2 pt-3 pb-2 border-top text-right" style="display: none">
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-default btn-paginate btn-prev">Prev</button>
                                <button type="button" class="btn btn-sm btn-default btn-paginate btn-next">Next</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 d-flex align-items-stretch">
                    <div class="w-100">
                        <div class="card border-0 shadow-sm p-3 mb-3 rounded-sm" style="background-color: var(--card-bg)">
                            <h5 class="border-bottom pb-2">Synchronization Details</h5>
                            <div id="salla-sync-info">
                                <div class="py-3 border-bottom">
                                    <button type="button" id="btn-sync-all" class="btn btn-xl btn-primary w-100 font-weight-bold py-3">Sync all Products</button>
                                </div>
                                <div class="product-count py-3 d-flex justify-content-stretch">
                                    <div class="text-center p-3 mx-2 rounded w-100" style="background-color: var(--bg-color)">
                                        <h2 id="count-products-salla">-</h2>
                                        <p class="text-muted m-0">in Salla</p>
                                    </div>
                                    <div class="text-center p-3 mx-2 rounded w-100" style="background-color: var(--bg-color)">
                                        <h2 id="count-products-erpnext">-</h2>
                                        <p class="text-muted m-0">in ERPNext</p>
                                    </div>
                                    <div class="text-center p-3 mx-2 rounded w-100" style="background-color: var(--bg-color)">
                                        <h2 id="count-products-synced">-</h2>
                                        <p class="text-muted m-0">Synced</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="card border-0 shadow-sm p-3 mb-3 rounded-sm" style="background-color: var(--card-bg); display: none;">
                            <h5 class="border-bottom pb-2">Sync Log</h5>
                            <div class="control-value like-disabled-input for-description overflow-auto" id="salla-sync-log" style="max-height: 500px;"></div>
                        </div>

                    </div>
                </div>
            </div>
        `);

		this.wrapper.append(_markup);

	}

	async fetchProductCount() {

		try {
			const { message: { syncedCount, erpnextCount } } = await frappe.call({ method: 'rukn_ecommerce.rukn_ecommerce.page.Api.get_product_count' });
			this.wrapper.find('#count-products-synced').text(syncedCount);
			this.wrapper.find('#count-products-erpnext').text(erpnextCount);

		} catch (error) {
			frappe.throw(__('Error fetching product count.'));
		}

	}

	async addTable() {

		const listElement = this.wrapper.find('#salla-product-list')[0];
		this.sallaProductTable = new frappe.DataTable(listElement, {
			columns: [
				// {
				//     name: 'Image',
				//     align: 'center',
				// },
				{
					name: 'ID',
					align: 'left',
					editable: false,
					focusable: false,
				},
				{
					name: 'Name',
					editable: false,
					focusable: false,
				},
				{
					name: 'SKUs',
					editable: false,
					focusable: false,
				},
				{
					name: 'Status',
					align: 'center',
					editable: false,
					focusable: false,
				},
				{
					name: 'Action',
					align: 'center',
					editable: false,
					focusable: false,
				},
			],
			data: await this.fetchSallaProducts(),
			layout: 'fixed',
		});

		this.wrapper.find('.salla-datatable-footer').show();
		this.wrapper.find('#count-products-salla').text(this.countProductsSalla);

	}

	async fetchSallaProducts(pagination_link = null) {

		try {
			const { message: { products, nextUrl, prevUrl, countProductsSalla } } = await frappe.call(
				{
					method: 'rukn_ecommerce.rukn_ecommerce.page.Api.get_salla_products',
					args: { pagination_link }
				}
			);
			this.nextUrl = nextUrl;
			this.prevUrl = prevUrl;

			this.countProductsSalla = countProductsSalla;

			return products.map((product) => ({
				// 'Image': product.image && product.image.src && `<img style="height: 50px" src="${product.image.src}">`,
				'ID': product.id,
				'Name': product.name,
				'SKUs': product.sku,
				'Status': this.getProductSyncStatus(product.synced),
				'Action': !product.synced ?
					`<button type="button" class="btn btn-default btn-xs btn-sync mx-2" data-product="${product.id}"> Sync </button>` :
					`<button type="button" class="btn btn-default btn-xs btn-resync mx-2" data-product="${product.id}"> Re-sync </button>`,
			}));
		} catch (error) {
			frappe.throw(__(error));
		}

	}

	getProductSyncStatus(status) {

		return status ?
			`<span class="indicator-pill green">Synced</span>` :
			`<span class="indicator-pill orange">Not Synced</span>`;

	}

	listen() {

		// sync a product from table
		this.wrapper.on('click', '.btn-sync', e => {

			const _this = $(e.currentTarget);

			_this.prop('disabled', true).text('Syncing...');

			const product_id = _this.attr('data-product');
			this.syncProduct(product_id)
				.then(status => {

					if (!status) {
						frappe.throw(__('Error syncing product'));
						_this.prop('disabled', false).text('Sync');
						return;
					}

					_this.parents('.dt-row')
						.find('.indicator-pill')
						.replaceWith(this.getProductSyncStatus(true));

                    _this.replaceWith(`<button type="button" class="btn btn-default btn-xs btn-resync mx-2" data-product="${product_id}"> Re-sync </button>`);

				});

		});

        this.wrapper.on('click', '.btn-resync', e => {
            const _this = $(e.currentTarget);

            _this.prop('disabled', true).text('Syncing...');

            const product_id = _this.attr('data-product');
            this.resyncProduct(product_id)
                .then(status => {

                    if (!status) {
                        frappe.throw(__('Error syncing product'));
                        return;
                    }

                    _this.parents('.dt-row')
                        .find('.indicator-pill')
                        .replaceWith(this.getProductSyncStatus(true));

                        _this.prop('disabled', false).text('Re-sync');

                })
                .catch(ex => {
                    _this.prop('disabled', false).text('Re-sync');
                    frappe.throw(__('Error syncing Product'));
                });
        });

		// pagination
		this.wrapper.on('click', '.btn-prev,.btn-next', e => this.switchPage(e));

		// sync all products
		this.wrapper.on('click', '#btn-sync-all', e => this.syncAll(e));

	}

	async syncProduct(product_id) {
		const { message: status } = await frappe.call({
			method: 'rukn_ecommerce.rukn_ecommerce.page.Api.sync_product',
			args: { product_id },
		});

		if (status)
			this.fetchProductCount();

		return status;

	}

    async resyncProduct(product_id) {

        const { message: status } = await frappe.call({
			method: 'rukn_ecommerce.rukn_ecommerce.page.Api.sync_product',
			args: { product_id },
		});

		if (status)
			this.fetchProductCount();

		return status;

    }

	async switchPage({ currentTarget }) {

		const _this = $(currentTarget);

		$('.btn-paginate').prop('disabled', true);
		this.sallaProductTable.showToastMessage('Loading...');

		const newProducts = await this.fetchSallaProducts(
			_this.hasClass('btn-next') ? this.nextUrl : this.prevUrl
		);

		this.sallaProductTable.refresh(newProducts);

		$('.btn-paginate').prop('disabled', false);
		this.sallaProductTable.clearToastMessage();

	}

}