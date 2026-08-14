document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("complaintSearch");

  const statusFilter = document.getElementById("statusFilter");

  const categoryFilter = document.getElementById("categoryFilter");

  const priorityFilter = document.getElementById("priorityFilter");

  const clearButton = document.getElementById("clearFilters");

  const complaintList = document.getElementById("complaintList");

  const noResults = document.getElementById("noResults");

  const resultsCount = document.getElementById("resultsCount");

  const pagination = document.getElementById("pagination");

  if (!complaintList) {
    return;
  }

  const complaints = Array.from(
    complaintList.querySelectorAll(".admin-complaint"),
  );

  const complaintsPerPage = 10;

  let currentPage = 1;

  let filteredComplaints = [...complaints];

  function applyFilters() {
    const searchText = searchInput.value.trim().toLowerCase();

    const selectedStatus = statusFilter.value.toLowerCase();

    const selectedCategory = categoryFilter.value.toLowerCase();

    const selectedPriority = priorityFilter.value.toLowerCase();

    filteredComplaints = complaints.filter(function (complaint) {
      const complaintId = complaint.dataset.complaintId || "";

      const student = complaint.dataset.student || "";

      const subject = complaint.dataset.subject || "";

      const status = (complaint.dataset.status || "").toLowerCase();

      const category = (complaint.dataset.category || "").toLowerCase();

      const priority = (complaint.dataset.priority || "").toLowerCase();

      const matchesSearch =
        searchText === "" ||
        complaintId.includes(searchText) ||
        student.includes(searchText) ||
        subject.includes(searchText);

      const matchesStatus = selectedStatus === "" || status === selectedStatus;

      const matchesCategory =
        selectedCategory === "" || category === selectedCategory;

      const matchesPriority =
        selectedPriority === "" || priority === selectedPriority;

      return (
        matchesSearch && matchesStatus && matchesCategory && matchesPriority
      );
    });

    currentPage = 1;

    renderComplaints();
  }

  function renderComplaints() {
    complaints.forEach(function (complaint) {
      complaint.style.display = "none";
    });

    if (filteredComplaints.length === 0) {
      complaintList.style.display = "none";

      noResults.style.display = "block";

      resultsCount.textContent = "Showing 0 complaints";

      pagination.innerHTML = "";

      return;
    }

    complaintList.style.display = "block";

    noResults.style.display = "none";

    const start = (currentPage - 1) * complaintsPerPage;

    const end = start + complaintsPerPage;

    const pageComplaints = filteredComplaints.slice(start, end);

    pageComplaints.forEach(function (complaint) {
      complaint.style.display = "";
    });

    const totalPages = Math.ceil(filteredComplaints.length / complaintsPerPage);

    resultsCount.textContent =
      "Showing " +
      (start + 1) +
      "-" +
      Math.min(end, filteredComplaints.length) +
      " of " +
      filteredComplaints.length +
      " complaints";

    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    pagination.innerHTML = "";

    if (totalPages <= 1) {
      return;
    }

    const previousButton = document.createElement("button");

    previousButton.type = "button";

    previousButton.className = "page-btn";

    previousButton.textContent = "← Previous";

    previousButton.disabled = currentPage === 1;

    previousButton.addEventListener("click", function () {
      if (currentPage > 1) {
        currentPage--;

        renderComplaints();
      }
    });

    pagination.appendChild(previousButton);

    const pageNumbers = document.createElement("div");

    pageNumbers.className = "page-numbers";

    for (let page = 1; page <= totalPages; page++) {
      const pageButton = document.createElement("button");

      pageButton.type = "button";

      pageButton.className = "page-number";

      if (page === currentPage) {
        pageButton.classList.add("active");
      }

      pageButton.textContent = page;

      pageButton.addEventListener("click", function () {
        currentPage = page;

        renderComplaints();
      });

      pageNumbers.appendChild(pageButton);
    }

    pagination.appendChild(pageNumbers);

    const nextButton = document.createElement("button");

    nextButton.type = "button";

    nextButton.className = "page-btn";

    nextButton.textContent = "Next →";

    nextButton.disabled = currentPage === totalPages;

    nextButton.addEventListener("click", function () {
      if (currentPage < totalPages) {
        currentPage++;

        renderComplaints();
      }
    });

    pagination.appendChild(nextButton);
  }

  searchInput.addEventListener("input", applyFilters);

  statusFilter.addEventListener("change", applyFilters);

  categoryFilter.addEventListener("change", applyFilters);

  priorityFilter.addEventListener("change", applyFilters);

  clearButton.addEventListener("click", function () {
    searchInput.value = "";

    statusFilter.value = "";

    categoryFilter.value = "";

    priorityFilter.value = "";

    applyFilters();
  });

  applyFilters();
});
